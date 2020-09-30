from rest_framework import serializers
from .models import Project, Game, User, Match, Player
from rest_framework.exceptions import APIException
from rest_framework import status
from django.db import IntegrityError


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'imgUrl',
        )


class CategorySerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'projectName', 'games',
        )


# class MatchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Match
#         fields = (
#             'id',
#             'game',
#             'maxPlayers',
#         )
#     def create(self, validated_data):
#         return Match.objects.create(**validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class Players(serializers.ModelSerializer):
    matchId = serializers.ReadOnlyField(source='room.id')
    userId = serializers.ReadOnlyField(source='playerName.id')

    class Meta:
        model = Player
        fields = (
            'userId', 'matchId',
        )
    def create(self, validated_data):
        return Player.objects.create(**validated_data)


class PlayersForMatch(serializers.ModelSerializer):
    userId = serializers.ReadOnlyField(source='playerName.id')
    playerName = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = (
            'userId', 'playerName',
        )



class CreateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            'id',
            'game',
            'maxPlayers',
        )

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

class MatchSerializer(serializers.ModelSerializer):
    players = PlayersForMatch(many=True)
    class Meta:
        model = Match
        fields = [
            'id',
            'maxPlayers',
            'players',
        ]

class RoomSerializer(serializers.ModelSerializer):
    matches = MatchSerializer(many=True)
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'matches',
        )
