import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

from library.consumers import ChatConsumer, EchoConsumer

django_asgi_app = get_asgi_application()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')



application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<str:username>/', ChatConsumer.as_asgi()),
                path('ws/chat/', EchoConsumer.as_asgi())
            ])
        )
    )
})

