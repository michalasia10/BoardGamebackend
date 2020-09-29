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
#             'playersNumber',
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


class MatchSerializer(serializers.ModelSerializer):
    players = Players(many=True)
    class Meta:
        model = Match
        fields = (
            'id',
            'game',
            'playersNumber',
            'players',
        )

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

class MatchSerial(serializers.ModelSerializer):
    players = Players(many=True)
    class Meta:
        model = Match
        fields = [
            'id',
            'game',
            'playersNumber',
            'players',
        ]

class RoomSerializer(serializers.ModelSerializer):
    rooms = MatchSerializer(many=True)

    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'rooms',
        )
