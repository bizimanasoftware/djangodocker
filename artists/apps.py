# artists/apps.py
from django.apps import AppConfig

class ArtistsConfig(AppConfig): # Renamed from DashboardAppConfig if it existed
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'artists' # Ensure this matches your app name
