from rest_framework import serializers
from .models import Project,Game



class GameSerializer(serializers.ModelSerializer):
    # game_category = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
    class Meta:
        model = Game
        fields = [
            'name',
            'playersNumber',
            'imgUrl',
        ]



class CategorySerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True,read_only=True)
    class Meta:
        model = Project
        fields = [
            'projectName','games',
        ]





