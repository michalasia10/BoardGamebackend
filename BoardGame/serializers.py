from rest_framework import serializers
from .models import Project,Game,User,Match,Player
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
    games = GameSerializer(many=True,read_only=True)
    class Meta:
        model = Project
        fields = (
            'projectName','games',
        )


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            'id',
            'game',
            'playersNumber',
        )
    def create(self, validated_data):
        return Match.objects.create(**validated_data)



class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

class Players(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'playerName',
        )

class RoomSerializer(serializers.ModelSerializer):
    rooms = MatchSerializer(many=True)
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'rooms',

        )
