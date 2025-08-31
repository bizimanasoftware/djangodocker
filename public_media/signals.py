# public_media/signals.py (or a new app for general signals)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import PublicMedia # Assuming PublicMedia model in public_media app
from notifications.models import Notification # Your Notification model

@receiver(post_save, sender=PublicMedia)
def create_public_media_notification(sender, instance, created, **kwargs):
    if created and instance.is_public: # Only notify on new public uploads
        # Create a database notification for admins or relevant users
        # You'll need logic to determine who should be notified (e.g., all admins)
        # For simplicity, let's notify a specific admin user or a group for now.
        # You might have an 'Admin' group or specific admin user IDs.
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_users = User.objects.filter(is_superuser=True) # Example: notify all superusers

        content_type = ContentType.objects.get_for_model(instance)
        link = f"/dashboards/public_media/{instance.id}/" # Link to the media item

        for admin_user in admin_users:
            # Create DB notification
            Notification.objects.create(
                recipient=admin_user,
                sender=instance.user, # The user who uploaded
                message=f"{instance.user.username} uploaded a new public media: {instance.title or instance.file.name}.",
                notification_type='new_public_media',
                related_object_content_type=content_type,
                related_object_id=instance.id,
                link_url=link
            )

            # Send real-time notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'notifications_{admin_user.id}',
                {
                    'type': 'send_notification',
                    'message': f"New public media from {instance.user.username}",
                    'notification_type': 'new_public_media',
                    'timestamp': instance.uploaded_at.isoformat(),
                    'link_url': link,
                    'sender_username': instance.user.username,
                }
            )
