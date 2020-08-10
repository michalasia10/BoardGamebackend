from rest_framework import serializers
from .models import Project,Game,Usernames
from rest_framework.exceptions import APIException
from rest_framework import status
from django.db import IntegrityError

class GameSerializer(serializers.ModelSerializer):
    # game_category = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'playersNumber',
            'imgUrl',
        )



class CategorySerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True,read_only=True)
    class Meta:
        model = Project
        fields = (
            'projectName','games',
        )






class Custom409(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A conflict occurred'

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Usernames
        fields = (
            'username',
        )

    def create(self, validated_data):
        return Usernames.objects.create(**validated_data)







