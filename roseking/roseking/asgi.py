"""
ASGI config for roseking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing
import waiting_room.routing
import game.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roseking.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(
      URLRouter(
          chat.routing.websocket_urlpatterns +
          waiting_room.routing.websocket_urlpatterns +
          game.routing.websocket_urlpatterns
      )
  ),
})
