from django.conf.urls import url

from .consumers import RoomConsumer

websocket_urlpatterns = [
    url(r'ws/room/(?P<match_pk>[0-9]+)$', RoomConsumer,name='room')
]