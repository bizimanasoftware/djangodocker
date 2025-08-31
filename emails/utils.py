# emails/utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_templated_email(subject, template_name, context, recipient_list, attachments=None):
    """
    Sends a templated HTML email with optional attachments.

    Args:
        attachments (list, optional): A list of tuples, where each tuple is
                                      (filename, file_content, content_type).
                                      Defaults to None.
    """
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        
        email = EmailMessage(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=recipient_list
        )
        email.attach_alternative(html_message, "text/html")

        # Add attachments if any
        if attachments:
            for filename, content, content_type in attachments:
                email.attach(filename, content, content_type)
        
        email.send(fail_silently=False)
        print(f"✅ Email sent successfully to {recipient_list}")
        return 1
    except Exception as e:
        print(f"🚨 Error sending email: {e}")
        return 0
