# public_media/models.py (or talents/models.py, profiles/models.py depending on your logical grouping)
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType # Already in settings

class PublicMedia(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='public_media')
    file = models.FileField(upload_to='public_media/%Y/%m/%d/') # Will go to S3
    file_type = models.CharField(
        max_length=10,
        choices=[('image', 'Image'), ('video', 'Video'), ('file', 'File')],
        default='image'
    )
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True,
                                    help_text="If unchecked, only the uploader and admins can see this media.")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Admin can provoke permissions - this is controlled by 'is_public' and the UserProfile's 'can_upload_public_media'

    class Meta:
        verbose_name_plural = "Public Media Items"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.user.username}'s {self.file_type}: {self.title or self.file.name}"

    @property
    def get_file_url(self):
        if self.file:
            return self.file.url
        return None
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file_type == 'image': # Or based on file size, etc.
            from public_media.tasks import process_image # Import task
            process_image.delay(self.id) # Call task asynchronously
