import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application  # ✅ Correct import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gloexproject.settings')
django.setup()  # ✅ Make sure Django is initialized

import messaging.routing  # ✅ AFTER django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # ✅ Use imported function
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messaging.routing.websocket_urlpatterns
        )
    ),
})
