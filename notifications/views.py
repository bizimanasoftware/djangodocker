# notifications/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This is a simple function-based view for the chat room.
# We're using the login_required decorator to ensure only
# authenticated users can access this page.
@login_required
def chat_room(request):
    """
    Renders the chat room template.
    """
    return render(request, 'notifications/room.html')
