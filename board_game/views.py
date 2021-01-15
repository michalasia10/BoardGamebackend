from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Game, User, Match, Player
from .serializers import CategorySerializer, GameSerializer, UserSerializerGet, UserSerializerPost, \
    CreateMatchSerializer, \
    RoomSerializer, \
    PlayersSerializerCreate, PlayersSerializerDetail, MatchSerializer
from django.shortcuts import get_object_or_404
from .multiserializer.multiserializer import MethodSerializerView
from django.db.models import Count


class CategoryList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


class RegisterUser(MethodSerializerView, generics.ListCreateAPIView):
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
        match_pk = player.match.pk
        match = get_object_or_404(Match, pk=match_pk)
        if match.status != 'ACTIVE':
            if player == match.players.last():
                match.delete()
                print(f"Match with id: {match_pk} deleted")
            player.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PlayerJoin(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayersSerializerCreate

    def create(self, request, *args, **kwargs):
        data = request.data
        match = get_object_or_404(Match, pk=data['match'])
        number = match.players.count()
        serializer = self.serializer_class(data=data)
        if number == match.maxPlayers and serializer.is_valid(raise_exception=True):
            serializer.save()
            match.status = 'ACTIVE'
            match.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'message': 'MATCH_FULL'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RoomDetail(APIView):
    def get(self, request, pk):
        match = get_object_or_404(Match, pk=pk)
        serializer = MatchSerializer(match)
        return Response(serializer.data)
