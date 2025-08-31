from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Thread, ChatMessage

User = get_user_model()

@login_required
def thread_list(request):
    """
    Displays a list of all active message threads for the logged-in user.
    """
    # Filters threads where the current user is one of the participants.
    # Q objects allow for complex queries with OR logic.
    threads = Thread.objects.filter(Q(participant1=request.user) | Q(participant2=request.user))

    context = {
        'threads': threads,
        'page_title': 'Messages',
    }
    return render(request, 'messaging/thread_list.html', context)

@login_required
def thread_detail(request, thread_id):
    """
    Displays a single message thread and its messages.
    Also handles the logic to determine if the user can send a message.
    """
    # Get the specific thread or return a 404 error if it doesn't exist
    thread = get_object_or_404(Thread, id=thread_id)
    
    # This is the crucial part:
    # Check if the current user is one of the participants in the thread.
    # We use this to set the `can_send_message` variable.
    can_send_message = (request.user == thread.participant1 or request.user == thread.participant2)
    
    # Get all messages associated with the thread, ordered by creation date
    thread_messages = ChatMessage.objects.filter(thread=thread).order_by('created')
    
    # Get the other participant in the chat for the page title
    other_participants = [user for user in [thread.participant1, thread.participant2] if user != request.user]

    context = {
        'thread': thread,
        'thread_messages': thread_messages,
        'other_participants': other_participants,
        'page_title': 'Conversation',
        'can_send_message': can_send_message, # This variable is passed to the template
    }
    return render(request, 'messaging/thread_detail.html', context)


@login_required
def create_or_find_thread(request, recipient_id):
    """
    Finds an existing thread or creates a new one between the current user
    and a specified recipient, then redirects to the thread's detail page.
    """
    # Get the user who will be the recipient of the message, or show a 404 error
    recipient = get_object_or_404(User, id=recipient_id)

    # Check if a thread already exists between the two users
    # We use a Q object with OR to check both possible participant orders.
    thread = Thread.objects.filter(
        Q(participant1=request.user, participant2=recipient) |
        Q(participant1=recipient, participant2=request.user)
    ).first()

    # If no thread exists, create a new one
    if not thread:
        thread = Thread.objects.create(
            participant1=request.user,
            participant2=recipient
        )

    # After finding or creating the thread, redirect to its detail view
    return redirect('messaging:thread_detail', thread_id=thread.id)
