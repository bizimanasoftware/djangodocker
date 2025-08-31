# settingspanel/urls.py
from django.urls import path
from . import views # You'll need to create these views

app_name = 'settingspanel' # <--- This is the crucial line for the namespace

urlpatterns = [
    path('', views.settings_home, name='settings_home'), # This matches 'settings_home'
    # Add other settings-related URLs here, e.g.,
    # path('profile-settings/', views.profile_settings, name='profile_settings'),
    # path('security-settings/', views.security_settings, name='security_settings'),
]
