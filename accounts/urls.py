# accounts/urls.py
from django.urls import path
from .views import UnifiedAuthView, RegistrationView, CustomLoginView, logout_view, \
    check_username_exists, check_email_exists # New imports

app_name = 'accounts'
urlpatterns = [
    # A single URL for the page that shows both login and registration forms
    path('auth/', UnifiedAuthView.as_view(), name='unified_auth'),

    # Hidden URLs that process the form submissions
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),

    # New URLs for AJAX frontend validation
    path('check-username/', check_username_exists, name='check_username_exists'),
    path('check-email/', check_email_exists, name='check_email_exists'),

    # URL for logging out
    path('logout/', logout_view, name='logout'),
]
