from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from BoardGame.models import Project, Game, User, Match, Player
from BoardGame.serializers import CategorySerializer, GameSerializer, UserSerializer, CreateMatchSerializer, RoomSerializer, \
    Players
from rest_framework.permissions import AllowAny
from rest_framework import renderers
from rest_framework import parsers
from django.shortcuts import get_object_or_404

class CategoryList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


class UserAPIView(APIView):
    # parser_classes = [JSONParser,]
    permission_classes = (AllowAny,)
    name = 'register'
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            print(error.data)
        return error


class CreateMatch(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = CreateMatchSerializer


class RoomList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = RoomSerializer


class PlayerDelete(APIView):
    def get(self,request,pk):
        player = get_object_or_404(Player,pk=pk)
        serializer = Players(player)
        return Response(serializer.data)
    def delete(self,request,pk):
        player = get_object_or_404(Player,pk=pk)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlayerJoin(APIView):
    def get(self, request):
        users = get_object_or_404(Player,matchID=request.matchID,userID=request.userID)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(matchID = request.matchID,userID=request.userID)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            print(error.data)
        return error