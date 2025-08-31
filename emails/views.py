# emails/views.py

import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

from .models import IncomingEmail, IncomingAttachment
from .forms import EmailComposerForm
from django.core.files.base import ContentFile
import base64

@method_decorator(csrf_exempt, name='dispatch')
@require_POST

def incoming_email_webhook(request):
    """
    Listens for incoming email webhooks from SMTP2GO.
    Parses the JSON payload and saves it, including attachments.
    """
    try:
        payload = json.loads(request.body)
        
        # Create the email record first
        email_instance = IncomingEmail.objects.create(
            subject=payload.get('subject', 'No Subject'),
            sender=payload.get('sender', 'unknown@sender.com'),
            recipient=payload.get('recipient', 'unknown@recipient.com'),
            body_plain=payload.get('text', ''),
            body_html=payload.get('html', ''),
            raw_payload=payload
        )
        
        # NEW: Check for and process attachments
        if 'attachments' in payload and payload['attachments']:
            for attachment_data in payload['attachments']:
                # Decode the Base64 encoded file content
                file_content = base64.b64decode(attachment_data.get('fileblob'))
                
                IncomingAttachment.objects.create(
                    email=email_instance,
                    file=ContentFile(file_content, name=attachment_data.get('filename')),
                    filename=attachment_data.get('filename', 'unknown_file'),
                    content_type=attachment_data.get('mimetype', 'application/octet-stream')
                )

        return JsonResponse({'status': 'success'}, status=200)

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)

# ... (rest of the file remains the same for now)


@staff_member_required
def email_composer_view(request):
    """A view within the admin to compose and send emails, with attachment support."""
    initial_data = {}
    
    # NEW: Handle "Reply" functionality
    reply_to_id = request.GET.get('reply_to')
    if reply_to_id:
        try:
            original_email = IncomingEmail.objects.get(id=reply_to_id)
            initial_data['recipients'] = original_email.sender
            initial_data['subject'] = f"Re: {original_email.subject}"
            quoted_body = f"\n\n\n--- On {original_email.received_at.strftime('%a, %b %d, %Y at %I:%M %p')}, {original_email.sender} wrote: ---\n> "
            quoted_body += original_email.body_plain.replace('\n', '\n> ')
            initial_data['body'] = quoted_body
        except IncomingEmail.DoesNotExist:
            messages.error(request, "The email you are trying to reply to does not exist.")

    if request.method == 'POST':
        # Don't forget to pass request.FILES to the form
        form = EmailComposerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                recipient_list = [email.strip() for email in form.cleaned_data['recipients'].split(',')]
                subject = form.cleaned_data['subject']
                body = form.cleaned_data['body']
                
                # Use EmailMessage to handle attachments
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=recipient_list,
                )

                # Attach uploaded files
                for f in request.FILES.getlist('attachments'):
                    email.attach(f.name, f.read(), f.content_type)
                
                email.send()
                
                messages.success(request, f"Email sent successfully to {', '.join(recipient_list)}.")
                return redirect('admin:emails_incomingemail_changelist')
            
            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")
    else:
        form = EmailComposerForm(initial=initial_data)

    return render(
        request,
        'admin/emails/composer.html',
        {'form': form, 'title': 'Compose Email'}
    )
