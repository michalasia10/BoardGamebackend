from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer
from .models import Match,Player
import json
from channels.db import database_sync_to_async
from .serializers import MatchSerializer
from django.shortcuts import get_object_or_404
from .game_logic.tictactoe import TicTacToe,State
from rest_framework import status
import random

class RoomConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, event):
        self.room_name = self.scope['url_route']['kwargs']['match_pk']
        self.room_group_name = self.room_name
        print(f"Connected, typ of connect {event}")
        print(self.room_group_name)
        match = await self.get_match(pk=self.room_name)
        numberOfPlayers = await self.get_match(pk=self.room_name,number=True)
        playersList = match['players']
        print(playersList)
        emptyMark = any(list(playersList[i].items())[2][1] == '' for i in range(len(playersList)))
        marks = list('XO')
        if emptyMark and (numberOfPlayers == match['maxPlayers']):
            for playerInfo in playersList:
                mark = random.choice(marks)
                playerInfoList = list(playerInfo.items())
                print(playerInfoList[0][1])
                playerId = playerInfoList[0][1]
                player = Player.objects.get(pk=playerId)
                print(player,mark)
                player.mark = mark
                marks.remove(mark)
                player.save(update_fields=['mark'])

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message',
                'data': match
            }
        )
        await self.accept()
        print(f"Hello, you're connected to BoardGames's websocket. "
              f"This room of id '{self.room_group_name}', has data as dict type : {match}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data, **kwargs):
        state = json.loads(text_data)
        match = await self.get_match(pk=self.room_name)
        playersList = match['players']
        print(f"JSON: {state}\nNew state of the game board: {state['boardState']}")
        new_state = state['boardState']
        game = State(match['state'], new_state)
        full_board = game.check_finished()
        one_move = game.check_move()
        blank_field = game.check_blank()
        if any(list(playersList[i].items())[2][1] == '' for i in range(len(playersList))):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'data': status.HTTP_400_BAD_REQUEST
                }
            )
        elif full_board:
            if not blank_field:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'message',
                        'data': status.HTTP_400_BAD_REQUEST
                    }
                )

        elif not one_move or not blank_field:
            print(f'Bad move, allowed 1 move : {one_move}/1 or you wanna try to change someone field {blank_field} ')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'data': status.HTTP_400_BAD_REQUEST
                }
            )
        elif blank_field:
             update_content = await self.get_match(pk=self.room_name, update=True, text=new_state)
             print(f"Updated content after ORM.update is {update_content}")



    async def newstate(self, event):
        dicta = json.loads(event['data'])
        await self.send(text_data=json.dumps(dicta))
        print(f' Automatically updated database content {dicta}')

    async def message(self, event):
        content = event['type']
        message = event["data"]
        await self.send(text_data=
        json.dumps(
            {
                'content': content,
                'data': message,
            }
        ))

    async def winner_message(self, event):
        winner = event['winner']
        if str(winner) in 'XO' or '':
            await self.get_match(pk=self.room_name, finish=True)
            match = await self.get_match(pk=self.room_name)
            await self.send(text_data=
            json.dumps(
                match
            ))
        await self.send(text_data=
        json.dumps(
            {
                'winner': winner,
            }
        ))

    @database_sync_to_async
    def get_match(self, pk, update=False, text=False, finish=False, created=False, number = False):
        match = get_object_or_404(Match, pk=pk)
        if update:
            match = Match.objects.get(pk=pk)
            match.state = text
            match.save(update_fields=['state'])
            return MatchSerializer(match).data
        if finish:
            match = Match.objects.get(pk=pk)
            match.status = 'FINISHED'
            match.save(update_fields=['status'])
        if created:
            match = Match.objects.get(pk=pk)
            match.status = 'ACTIVE'
            match.save(update_fields='status')
        if number:
            return match.players.count()
        else:
            return MatchSerializer(match).data
