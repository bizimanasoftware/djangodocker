# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This URL will link to your chat room view
    path('chat/', views.chat_room, name='chat_room'),
]
