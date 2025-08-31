# chat_with_admin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import AdminChatMessage
from django.contrib.auth import get_user_model
from .forms import ContactForm  # <--- Import your new ContactForm
from django.contrib import messages
User = get_user_model()


def is_admin(user):
    return user.is_staff


def user_can_chat(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if hasattr(request.user, 'can_access_chat') and not request.user.can_access_chat:
            messages.error(request, "You do not have permission to access the chat system.")
            return redirect('dashboard') # Or any appropriate redirect for forbidden access
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_content = form.cleaned_data['message']

            # Combine subject into the message content for clarity in chat inbox
            full_message_for_admin = f"Subject: {subject}\n\n{message_content}" if subject else message_content

            # Create a new AdminChatMessage instance
            AdminChatMessage.objects.create(
                user=None, # This is an anonymous message, so no linked registered user
                anonymous_sender_name=name,
                anonymous_sender_email=email,
                sender_is_admin=False, # This message is from a non-admin
                message=full_message_for_admin,
                is_read_by_admin=False, # New message, so it's unread by admin
                is_read_by_user=True, # The sender (user) has "sent" it, so they conceptually "read" their own initial message
            )
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('chat_with_admin:contact_us') # Redirect to clear POST data and show success message
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm() # Initialize an empty form for GET request

    context = {
        'form': form,
    }
    return render(request, 'chat_with_admin/contact_us.html', context)

@login_required
@user_can_chat # Apply this decorator for regular user's chat view
def admin_chat_view(request):
    messages_list = AdminChatMessage.objects.filter(user=request.user).order_by('timestamp')
    AdminChatMessage.objects.filter(user=request.user, sender_is_admin=True, is_read_by_user=False).update(is_read_by_user=True)

    context = {
        'messages': messages_list,
        'current_user': request.user,
    }
    return render(request, 'chat_with_admin/user_chat.html', context)


@login_required
@user_can_chat # Apply this decorator for message sending view
def send_admin_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message', '').strip()
        user_id = request.POST.get('user_id')

        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not message_content:
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': 'Message cannot be empty.'}, status=400)
            else:
                messages.error(request, 'Message cannot be empty.')
                if is_admin(request.user) and user_id:
                    return redirect('chat_with_admin:admin_chat_detail', user_id=user_id)
                else:
                    return redirect('chat_with_admin:admin_chat')


        target_user = request.user
        sender_is_admin = False

        if is_admin(request.user):
            if not user_id:
                if is_ajax:
                    return JsonResponse({'status': 'error', 'message': 'User ID required for admin replies.'}, status=400)
                else:
                    messages.error(request, 'User ID required for admin replies.')
                    return redirect('chat_with_admin:admin_dashboard')

            try:
                target_user = get_object_or_404(User, id=user_id)
            except User.DoesNotExist:
                if is_ajax:
                    return JsonResponse({'status': 'error', 'message': 'Target user not found.'}, status=404)
                else:
                    messages.error(request, 'Target user not found.')
                    return redirect('chat_with_admin:admin_dashboard')

            sender_is_admin = True
            AdminChatMessage.objects.filter(user=target_user, sender_is_admin=False, is_read_by_admin=False).update(is_read_by_admin=True)

        else:
            target_user = request.user
            sender_is_admin = False
            AdminChatMessage.objects.filter(user=request.user, sender_is_admin=True, is_read_by_user=False).update(is_read_by_user=True)


        AdminChatMessage.objects.create(
            user=target_user,
            sender_is_admin=sender_is_admin,
            message=message_content,
            is_read_by_user=False if sender_is_admin else True,
            is_read_by_admin=False if not sender_is_admin else True
        )

        if is_ajax:
            return JsonResponse({"status": "success", "message": "Message sent."})
        else:
            messages.success(request, "Message sent successfully!")
            if is_admin(request.user) and user_id:
                return redirect('chat_with_admin:admin_chat_detail', user_id=target_user.pk)
            else:
                return redirect('chat_with_admin:admin_chat')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
    else:
        messages.error(request, "Invalid request method.")
        if request.user.is_authenticated and is_admin(request.user):
             return redirect('chat_with_admin:admin_dashboard')
        elif request.user.is_authenticated:
             return redirect('chat_with_admin:admin_chat')
        else:
            return redirect('login')


# chat_with_admin/views.py (within the admin_chat_dashboard function)

@user_passes_test(is_admin)
def admin_chat_dashboard(request):
    """
    Admin-facing view to see a list of users with active chats.
    This would typically show users who have unread messages for the admin.
    """
    # Get users who have sent messages that admin hasn't read yet, or just any users who have chatted
    # REMOVED .order_only('username', 'id') as it's not a valid QuerySet method
    users_with_messages = User.objects.filter(
        admin_chat_messages__isnull=False
    ).distinct().order_by('username') # <--- CORRECTED LINE

    # You could further annotate this to show unread counts for each user
    users_with_unread = []
    for user in users_with_messages:
        unread_count = AdminChatMessage.objects.filter(
            user=user,
            sender_is_admin=False, # Messages sent by user
            is_read_by_admin=False # Unread by admin
        ).count()
        users_with_unread.append({'user': user, 'unread_count': unread_count})

    context = {
        'users_with_unread': users_with_unread
    }
    return render(request, 'chat_with_admin/admin_dashboard.html', context)

@user_passes_test(is_admin)
def admin_chat_detail_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    messages_list = AdminChatMessage.objects.filter(user=target_user).order_by('timestamp')

    AdminChatMessage.objects.filter(user=target_user, sender_is_admin=False, is_read_by_admin=False).update(is_read_by_admin=True)

    context = {
        'target_user': target_user,
        'messages': messages_list,
        'current_user': request.user,
    }
    return render(request, 'chat_with_admin/admin_chat_detail.html', context)
