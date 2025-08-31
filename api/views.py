# api/views.py (Add to your existing api app)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import mimetypes
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from messaging.models import Message # If this view also handles chat media uploads
from public_media.models import PublicMedia # Assuming PublicMedia is here for profile media

@csrf_exempt # Only if you handle CSRF differently or for simple API for now. For production APIs, use DRF and proper authentication.
@login_required
def upload_chat_media_api(request):
    if request.method == 'POST':
        if not request.user.user_profile.can_send_messages: # Check permission to send messages (which implies media too)
            return JsonResponse({'error': 'You do not have permission to send media.'}, status=403)

        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)

        # Determine file type
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        file_type = 'file'
        if mime_type:
            if mime_type.startswith('image/'):
                file_type = 'image'
            elif mime_type.startswith('video/'):
                file_type = 'video'

        # Define path within S3 bucket
        file_name = default_storage.save(f'chat_media/{uploaded_file.name}', uploaded_file)
        file_url = default_storage.url(file_name)

        return JsonResponse({
            'media_url': file_url,
            'file_name': uploaded_file.name,
            'file_type': file_type,
            'message': 'File uploaded successfully.' # Optional, if message content also comes
        })
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt # Again, for simple API. For production, use DRF.
@login_required
def upload_public_profile_media_api(request):
    if request.method == 'POST':
        if not request.user.user_profile.can_upload_public_media: # Check permission
            return JsonResponse({'error': 'You do not have permission to upload public media.'}, status=403)

        uploaded_file = request.FILES.get('file')
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        is_public_str = request.POST.get('is_public', 'true').lower()
        is_public = is_public_str == 'true' or is_public_str == '1'

        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)

        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        file_type = 'file'
        if mime_type:
            if mime_type.startswith('image/'):
                file_type = 'image'
            elif mime_type.startswith('video/'):
                file_type = 'video'

        # Save to PublicMedia model, which handles S3 upload
        try:
            public_media_item = PublicMedia.objects.create(
                user=request.user,
                file=uploaded_file, # This automatically uses S3 storage
                file_type=file_type,
                title=title,
                description=description,
                is_public=is_public
            )
            return JsonResponse({
                'status': 'success',
                'media_url': public_media_item.get_file_url,
                'media_id': public_media_item.id,
                'message': 'Public media uploaded successfully.'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
