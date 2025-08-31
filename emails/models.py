# emails/models.py

from django.db import models
from django.conf import settings
import uuid
# This function defines the upload path for attachments
def attachment_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/email_attachments/<uuid>/<filename>
    return f'email_attachments/{instance.email.id}/{uuid.uuid4()}_{filename}'

class IncomingEmail(models.Model):
    """Stores emails received via the SMTP2GO webhook."""
    subject = models.CharField(max_length=255, blank=True)
    sender = models.EmailField(max_length=255)
    recipient = models.EmailField(max_length=255)
    body_plain = models.TextField(blank=True, help_text="Plain text version of the email body.")
    body_html = models.TextField(blank=True, help_text="HTML version of the email body.")
    received_at = models.DateTimeField(auto_now_add=True)
    raw_payload = models.JSONField(help_text="The full, raw JSON payload from the webhook.")

    def __str__(self):
        return f"From: {self.sender} | To: {self.recipient} | Subject: {self.subject}"

    class Meta:
        verbose_name = "Received Email"
        verbose_name_plural = "Inbox (Received Emails)"
        ordering = ['-received_at']
    pass
class IncomingAttachment(models.Model):
    """Stores a single attachment file related to an IncomingEmail."""
    email = models.ForeignKey(
        IncomingEmail, 
        on_delete=models.CASCADE, 
        related_name='attachments'
    )
    file = models.FileField(upload_to=attachment_upload_path)
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)

    def __str__(self):
        return self.filename

class EmailDraft(models.Model):
    """Allows admins to compose and save email drafts."""
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='email_drafts'
    )
    recipient = models.CharField(max_length=500, help_text="Comma-separated email addresses.")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Draft for: {self.recipient} | Subject: {self.subject}"

    class Meta:
        verbose_name = "Email Draft"
        verbose_name_plural = "Email Drafts"
        ordering = ['-updated_at']
    pass
