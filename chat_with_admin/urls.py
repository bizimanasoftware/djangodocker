from django.urls import path # No need for 'include' here
from . import views

app_name = 'chat_with_admin' # This is crucial for namespacing

urlpatterns = [
    # User-facing chat and Contact Form (no 'admin-chat/' prefix here)
    path('contact/', views.contact_us_view, name='contact_us'), # Correctly placed at the app's root

    # Admin Dashboard & Chat Views (these will have the 'admin-chat/' prefix)
    path('admin-chat/', views.admin_chat_view, name='admin_chat'), # Main admin chat view
    path('admin-chat/send/', views.send_admin_message, name='send_admin_message'),
    path('admin-chat/dashboard/', views.admin_chat_dashboard, name='admin_dashboard'), # Primary dashboard view
    path('admin-chat/detail/<int:user_id>/', views.admin_chat_detail_view, name='admin_chat_detail'), # Detail view for a specific user's chat

    # Removed the duplicate 'admin-chat/dashboard/' and the problematic self-inclusion line
    # path('chat/', include('chat_with_admin.urls', namespace='chat_with_admin')) <-- REMOVE THIS LINE!
]
