"""
    ASGI (Asynchronous Server Gateway Interface) is a spiritual successor to WSGI, intended to provide
    a standard interface between async-capable Python web servers, frameworks, and applications. Where
    WSGI provided a standard for synchronous Python apps, ASGI provides one for both asynchronous and
    synchronous apps, with a WSGI backwards-compatibility implementation and multiple servers and
    application frameworks.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhossc.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
