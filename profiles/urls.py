# /home/deploy/gloexproject/profiles/urls.py
# URL configuration for the profiles application.

from django.urls import path
from . import views

app_name='profiles'
urlpatterns = [
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/gallery/', views.manage_gallery, name='manage_gallery'),

    # Public URLs
    path('discover/', views.discover_profiles, name='discover_profiles'),
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('<int:pk>/<str:action>/request/', views.sponsorship_request_view, name='sponsorship_request'),
    path('<int:pk>/request/submitted/', views.request_submitted, name='request_submitted'),

    # Comment URLs for professional handling
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
