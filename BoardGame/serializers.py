from rest_framework import serializers
from .models import Project,Game,Usernames



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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usernames
        fields = (
            'username',
        )

    def create(self, validated_data):
        return Usernames.objects.create(**validated_data)





