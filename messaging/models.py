from django.db import models
from django.contrib.auth import get_user_model

# Get the custom user model (if it exists) or the default Django user model
User = get_user_model()

class Thread(models.Model):
    """
    Represents a conversation thread between two users.
    """
    # Foreign key to the User model, for the first participant in the thread
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads_as_participant1')
    # Foreign key to the User model, for the second participant in the thread
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads_as_participant2')
    # An auto-updating timestamp to track when the thread was last updated
    updated = models.DateTimeField(auto_now=True)
    # An auto-set timestamp for when the thread was created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Enforce that no two threads can exist with the same pair of participants
        unique_together = ('participant1', 'participant2',)
        # Order the threads with the most recently updated at the top
        ordering = ('-updated',)

    def __str__(self):
        return f'Thread between {self.participant1.username} and {self.participant2.username}'

class ChatMessage(models.Model):
    """
    Represents a single message within a conversation thread.
    """
    # Foreign key to the Thread model
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    # Foreign key to the User model, to track who sent the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # The actual text of the message
    text = models.TextField()
    # An auto-set timestamp for when the message was created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order the messages within a thread by creation date
        ordering = ('created',)

    def __str__(self):
        return f'Message from {self.sender.username} in thread {self.thread.id}'
