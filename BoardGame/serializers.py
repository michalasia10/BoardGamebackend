from rest_framework import serializers
from .models import Project, Game, User, Match, Player


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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class PlayersSerializerCreate(serializers.ModelSerializer):
    match = serializers.PrimaryKeyRelatedField(many=False, queryset=Match.objects.all())
    playerName = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())

    class Meta:
        model = Player
        fields = (
            'match', 'playerName',
        )

    def create(self, validated_data):
        return Player.objects.create(match=validated_data['match'], playerName=validated_data['playerName'])


class PlayersSerializerDetail(serializers.ModelSerializer):
    matchId = serializers.IntegerField(source='match.id')
    userId = serializers.IntegerField(source='playerName.id')

    class Meta:
        model = Player
        fields = (
            'userId', 'matchId',
        )


class PlayersSerializerForMatch(serializers.ModelSerializer):
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
    players = PlayersSerializerForMatch(many=True)

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
