from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path
from ecgwebsite import consumer

websocket_urlPattern=[
    path('polData',consumer.DashConsumer),
]

application=ProtocolTypeRouter({
 
    'websocket':AuthMiddlewareStack(URLRouter(websocket_urlPattern))
})