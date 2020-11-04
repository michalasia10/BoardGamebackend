from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import  BoardGame.routing
from .wsgi import *

application = ProtocolTypeRouter({
    'websocket':  AuthMiddlewareStack(
        URLRouter(
            BoardGame.routing.websocket_urlpatterns
        )
    )
})
# channel_routing = {}
