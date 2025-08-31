# messaging/urls.py
from django.urls import path

from . import views

app_name = 'messaging'

urlpatterns = [
    # Displays a list of all chat threads for the user
    path('', views.thread_list, name='thread_list'),
    
    # Displays the messages within a specific thread
    path('<int:thread_id>/', views.thread_detail, name='thread_detail'),
    
    # New: This path will start a new thread with a specific user,
    # or find and redirect to an existing one.
    path('start-chat/<int:recipient_id>/', views.create_or_find_thread, name='create_or_find_thread'),
]
