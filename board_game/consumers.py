from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Match
import json
from channels.db import database_sync_to_async
from .serializers import MatchSerializer
from django.shortcuts import get_object_or_404


class RoomConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, event):
        self.room_name = self.scope['url_route']['kwargs']['match_pk']
        self.room_group_name = self.room_name
        print(f"Connected, typ of connect {event}")
        match = await self.get_match(pk=self.room_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message',
                'data': match
            }
        )
        print(f"Hello, you're connected to BoardGames's websocket. "
              f"This room of id '{self.room_group_name}', has data as dict type : {match}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data, **kwargs):
        state = json.loads(text_data)
        print(f"JSON: {state}\nNew state of the game board: {state['boardState']}")
        self.text = state['boardState']
        update_content = await self.get_match(pk=self.room_name, update=True)
        # await self.send(text_data=json.dumps({'cos':message}))
        print(f"Updated content after ORM.update is {update_content}")

    async def newstate(self, event):
        dicta = json.loads(event['data'])
        await self.send(json.dumps(dicta))
        print(f' Automatically updated database content {dicta}')

    async def message(self, event):
        content = event['type']
        something = event["data"]
        await self.send(text_data=
        json.dumps(
            {
                'content': content,
                'data': something,
            }
        ))

    @database_sync_to_async
    def get_match(self, pk, update=False):
        match = get_object_or_404(Match, pk=pk)
        if update:
            match = Match.objects.get(pk=pk)
            match.state = self.text
            match.save(update_fields=['state'])
            return MatchSerializer(match).data
        else:
            return MatchSerializer(match).data
