from django.conf.urls import url

from .consumers import RoomConsumer

websocket_urlpatterns = [
    url(r'ws/match/(?P<match_pk>[0-9]+)$', RoomConsumer.as_asgi(),name='room')
]