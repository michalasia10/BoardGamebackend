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
        await self.accept()
        print(f"Connected, typ of connect {event}")
        print(self.room_group_name)
        match = await self.get_match(pk=self.room_name)
        numberOfPlayers = await self.players_number(pk=self.room_name)
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
                if mark == 'X':
                    await self.change_current_player(pk=self.room_name,current=playerId)
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
        # await self.accept()
        print(f"Hello, you're connected to BoardGames's websocket. "
              f"This room of id '{self.room_group_name}', has data as dict type : {match}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data, **kwargs):
        data = json.loads(text_data)
        match = await self.get_match(pk=self.room_name)
        playersList = match['players']
        playerId = data['playerId']
        print(f"JSON: {data}\nNew data of the game board: {data['boardState']}")
        new_state = data['boardState']
        game = State(match['state'], new_state)
        full_board = game.check_finished()
        one_move = game.check_move()
        blank_field = game.check_blank()
        new_mark = game.check_mark()
        currentPlayerMark = await self.get_player(pk=match['currentPlayer'])
        print('new mark', new_mark, currentPlayerMark)
        print(currentPlayerMark==new_mark)
        if any(list(playersList[i].items())[2][1] == '' for i in range(len(playersList))):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'data': status.HTTP_400_BAD_REQUEST
                }
            )
        elif full_board and playerId == match['currentPlayer'] and currentPlayerMark == new_mark:
                print('tu zmiana')
                await self.update_match(pk=self.room_name,text=new_state)


        elif not one_move or not blank_field:
            print(f'Bad move, allowed 1 move : {one_move}/1 or you wanna try to change someone field {blank_field} ')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'data': status.HTTP_400_BAD_REQUEST
                }
            )
         # check if move was correct and playerId is the same as currentPlayer
        elif blank_field:
            print('dupa')
            if playerId == match['currentPlayer'] and currentPlayerMark == new_mark:
                enemyPlayerId = [list(i.items())[0][1] for i in playersList if list(i.items())[0][1] != playerId][0]
                update_content = await self.update_match(pk=self.room_name, text=new_state, enemyPlayerId=enemyPlayerId)
                print(f"Enemy Player Id : {enemyPlayerId}, Updated content after ORM.update is {update_content}")
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'message',
                        'data': status.HTTP_400_BAD_REQUEST
                    }
                )



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
            await self.update_match_status(pk=self.room_name, status='FINISHED')
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
    def get_match(self, pk):
        match = get_object_or_404(Match, pk=pk)
        return MatchSerializer(match).data

    @database_sync_to_async
    def update_match(self,pk,text, enemyPlayerId=False):
        match = get_object_or_404(Match, pk=pk)
        match.state = text
        if enemyPlayerId:
            match.currentPlayer = enemyPlayerId
            match.save(update_fields=['state','currentPlayer'])
        else:
            match.save(update_fields=['state'])
        return MatchSerializer(match).data

    @database_sync_to_async
    def update_match_status(self,pk,status):
        match = get_object_or_404(Match, pk=pk)
        if status == 'FINISHED':
            match.status = 'FINISHED'
            match.save(update_fields=['status'])
        elif status == 'ACTIVE':
            match.status = 'ACTIVE'
            match.save(update_fields='status')

    @database_sync_to_async
    def players_number(self,pk):
        match = get_object_or_404(Match, pk=pk)
        return match.players.count()

    @database_sync_to_async
    def change_current_player(self,pk,current):
        match = get_object_or_404(Match, pk=pk)
        match.currentPlayer = current
        match.save(update_fields=['currentPlayer'])

    @database_sync_to_async
    def get_player(self, pk):
        player = get_object_or_404(Player,pk=pk)
        return player.mark