"""
ASGI config for groomeet project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from groomeet_backend import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'groomeet.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            groomeet_backend.routing.websocket_urlpatterns
        )
    ),
})
