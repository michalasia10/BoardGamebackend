from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from BoardGame.models import Project, Game, User, Match, Player
from BoardGame.serializers import CategorySerializer, GameSerializer, UserSerializerGet, UserSerializerPost,CreateMatchSerializer, \
    RoomSerializer, \
    PlayersSerializerCreate,PlayersSerializerDetail
from rest_framework.permissions import AllowAny
from rest_framework import renderers
from rest_framework import parsers
from django.shortcuts import get_object_or_404
from .multiserializer.multiserializer import MethodSerializerView

class CategoryList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


class RegisterUser(MethodSerializerView,generics.ListCreateAPIView):
    queryset = User.objects.all()
    method_serializer_classes = {
        'GET': UserSerializerGet,
        'POST': UserSerializerPost
    }

class CreateMatch(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = CreateMatchSerializer


class RoomList(APIView):
    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = RoomSerializer(game)
        return Response(serializer.data)


class AllMatches(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = RoomSerializer


class PlayerDelete(APIView):
    def get(self, request, pk):
        player = get_object_or_404(Player, pk=pk)
        serializer = PlayersSerializerDetail(player)
        return Response(serializer.data)

    def delete(self, request, pk):
        player = get_object_or_404(Player, pk=pk)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerJoin(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayersSerializerCreate


