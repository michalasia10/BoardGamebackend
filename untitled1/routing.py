from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import  board_game.routing
from .wsgi import *

application = ProtocolTypeRouter({
    'websocket':  AuthMiddlewareStack(
        URLRouter(
            board_game.routing.websocket_urlpatterns
        )
    )
})
# channel_routing = {}
