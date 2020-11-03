from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import  BoardGame.routing


application = ProtocolTypeRouter({
    'websocket':  AuthMiddlewareStack(
        URLRouter(
            BoardGame.routing.websocket_urlpatterns
        )
    )
})