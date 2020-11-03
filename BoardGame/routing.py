from django.urls import re_path

from .consumers import RoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<match_pk>[0-9]+)$', RoomConsumer,name='room')
]