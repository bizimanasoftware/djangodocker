# updates/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    # ... (no changes to this model)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='published_at', blank=True)

    # Main Content
    body = RichTextUploadingField(help_text="Main content of the post. You can upload images directly.")
    featured_image = CloudinaryField('image', blank=True, null=True, help_text="A primary image for the post.")
    featured_video = CloudinaryField('video', resource_type='video', blank=True, null=True, help_text="A primary video for the post.")
    
    # MODIFIED: This now saves to your server's 'media' directory
    attachment = models.FileField(upload_to='post_attachments/', blank=True, null=True, help_text="Attach a PDF or other document.")

    # Styling & Formatting
    title_color = models.CharField(max_length=7, default='#000000', help_text="Hex color code for the title (e.g., #FF5733).")
    font_size = models.PositiveIntegerField(default=32, help_text="Font size for the title in pixels.")
    underline_title = models.BooleanField(default=False)

    # Publishing
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(default=timezone.now, help_text="You can set a future date to schedule the post.")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('updates:post_detail', args=[self.published_at.year, self.published_at.month, self.published_at.day, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# NEW: Model for the image gallery
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='gallery_images')
    image = CloudinaryField('image', help_text="Upload an image for the post gallery.")
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for post: {self.post.title}"
