"""
ASGI config for dawnWeb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path
from ecgwebsite import consumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dawnWeb.settings')

django_asgi_app = get_asgi_application()

websocket_urlPattern=[
    path('polData',consumer.DashConsumer),
]
application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(URLRouter(websocket_urlPattern)),
  
})

