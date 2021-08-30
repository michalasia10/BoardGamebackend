from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from board_game.models import Game,Match
from board_game.serializers import RoomSerializerWithAllStates, RoomSerializerWithoutFinished,MatchesForPlayer


class MatchesHistory(APIView):
    def get(self, request, ):
        gameId = request.GET.get('gameId', None)
        userId = request.GET.get('userId', None)
        if userId and gameId:
            game = Game.objects.all()
            serializer = MatchesForPlayer(game,context={'userId':userId,'gameId':gameId})
            return Response(serializer.data)
        if gameId:
            game = get_object_or_404(Game, pk=gameId)
            serializer = RoomSerializerWithoutFinished(game)
            return Response(serializer.data)
        if userId:
            game = Game.objects.all()
            print(game)
            serializer = MatchesForPlayer(game,context={'userId':userId})
            return Response(serializer.data)
        else:
            queryset = Game.objects.all()
            serializer = RoomSerializerWithAllStates(queryset,many=True)
            return Response(serializer.data)




