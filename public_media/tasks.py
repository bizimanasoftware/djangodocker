# public_media/tasks.py
from celery import shared_task
from PIL import Image # For image processing
from django.core.files.storage import default_storage
import os
from io import BytesIO

@shared_task
def process_image(media_id):
    from .models import PublicMedia # Import locally to avoid circular imports

    try:
        media_item = PublicMedia.objects.get(id=media_id)
        if media_item.file_type == 'image':
            img_file = default_storage.open(media_item.file.name, 'rb')
            img = Image.open(img_file)

            # Example: Resize image to max 800px width, maintain aspect ratio
            max_width = 800
            if img.width > max_width:
                new_height = int((max_width / img.width) * img.height)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Save back to S3 (overwrite original or save as new version)
            # For simplicity, let's overwrite for now.
            # In production, you might save as a 'thumbnail' or 'web_optimized' version.
            buffer = BytesIO()
            img_format = img.format if img.format else 'JPEG' # Default to JPEG if unknown
            img.save(buffer, format=img_format)
            default_storage.save(media_item.file.name, ContentFile(buffer.getvalue()))

            img_file.close()
            print(f"Processed image: {media_item.file.name}")
        # You'd add video transcoding logic here, possibly calling external APIs
    except PublicMedia.DoesNotExist:
        print(f"Media item {media_id} not found.")
    except Exception as e:
        print(f"Error processing media {media_id}: {e}")
