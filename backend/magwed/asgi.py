"""
ASGI config for magwed project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from accounts.middleware import WebSocketAuthMiddleware
import messenger.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magwed.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        WebSocketAuthMiddleware(
            URLRouter(
                messenger.routing.websocket_urlpatterns
            )
        )
    ),
})
