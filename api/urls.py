# api/urls.py (Add to your existing api app)
from django.urls import path
from . import views

app_name = 'api' # Make sure your api app has an app_name

urlpatterns = [
    path('upload_chat_media/', views.upload_chat_media_api, name='upload_chat_media'),
    path('upload_public_profile_media/', views.upload_public_profile_media_api, name='upload_public_profile_media'),
    # ... other API endpoints you might have
]
