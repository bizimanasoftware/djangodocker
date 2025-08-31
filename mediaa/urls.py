from django.urls import path
from .views import upload_media

app_name = "media"

urlpatterns = [
    path('upload/', upload_media, name="upload"),
]
