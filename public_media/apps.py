# public_media/apps.py (assuming you have a public_media app for user uploads)
from django.apps import AppConfig

class PublicMediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'public_media' # Or 'talents' or 'profiles' where this model resides

    def ready(self):
        import public_media.signals # Import your signals file
