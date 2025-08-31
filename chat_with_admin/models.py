from django.contrib.auth.models import AbstractUser

# chat_with_admin/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class AdminChatMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_chat_messages',
        verbose_name='User',
        null=True,     # <--- Allow NULL for anonymous messages
        blank=True     # <--- Allow blank in forms for anonymous messages
    )
    # New fields for anonymous senders from Contact Us form
    anonymous_sender_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Anonymous Sender Name",
        help_text="Name if sender is not a registered user."
    )
    anonymous_sender_email = models.EmailField(
        blank=True,
        verbose_name="Anonymous Sender Email",
        help_text="Email if sender is not a registered user."
    )

    sender_is_admin = models.BooleanField(
        default=False,
        verbose_name='Sent by Admin'
    )
    message = models.TextField(
        verbose_name='Message Content'
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Sent At'
    )
    # is_read_by_user will be True for contact form senders as they just sent it
    is_read_by_user = models.BooleanField(
        default=False,
        verbose_name='Read by User'
    )
    # is_read_by_admin should be False for new contact form messages
    is_read_by_admin = models.BooleanField(
        default=False,
        verbose_name='Read by Admin'
    )

    class Meta:
        verbose_name = 'Admin Chat Message'
        verbose_name_plural = 'Admin Chat Messages' # <--- Corrected this line
        ordering = ['timestamp']

    def __str__(self):
        if self.sender_is_admin:
            sender = "Admin"
        elif self.user:
            sender = self.user.username
        else: # Anonymous sender
            sender = self.anonymous_sender_name if self.anonymous_sender_name else "Anonymous"
            if self.anonymous_sender_email:
                sender += f" ({self.anonymous_sender_email})"

        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {sender}: {self.message[:50]}..."

    # Helper method to get the sender's display name for templates/admin
    def get_sender_display(self):
        if self.sender_is_admin:
            return "Admin"
        elif self.user:
            return self.user.username
        elif self.anonymous_sender_name:
            return self.anonymous_sender_name
        elif self.anonymous_sender_email:
            return self.anonymous_sender_email
        return "Anonymous"

    # Helper method to get the sender's email for potential replies
    def get_sender_email(self):
        if self.user and self.user.email:
            return self.user.email
        elif self.anonymous_sender_email:
            return self.anonymous_sender_email
        return None # No email available
# accounts/models.py (Example if you have a custom user model)

class CustomUser(AbstractUser):
    # ... existing fields ...
    can_access_chat = models.BooleanField(default=True, verbose_name="Can Access Chat System")

    def __str__(self):
        return self.username
