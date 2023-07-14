"""
    ASGI (Asynchronous Server Gateway Interface) is a spiritual successor to WSGI, intended to provide
    a standard interface between async-capable Python web servers, frameworks, and applications. Where
    WSGI provided a standard for synchronous Python apps, ASGI provides one for both asynchronous and
    synchronous apps, with a WSGI backwards-compatibility implementation and multiple servers and
    application frameworks.
"""

# import os
#
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import chat.routing
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhossc.settings')
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application
from django.urls import path

from chat.consumers import ChatConsumer
import chat.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhossc.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})