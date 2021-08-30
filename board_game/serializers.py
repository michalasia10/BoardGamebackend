from django.db.models import Q
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


class UserSerializerPost(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserSerializerGet(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


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
            'userId', 'playerName','mark',
        )


class CreateMatchSerializer(serializers.ModelSerializer):
    # game = serializers.PrimaryKeyRelatedField(many=False,queryset=Game.objects.all())
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
            'state',
            'currentPlayer',
            'status',
        ]


class RoomSerializerWithAllStates(serializers.ModelSerializer):
    matches = MatchSerializer(many=True)

    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'matches',
        )


class RoomSerializerWithoutFinished(serializers.ModelSerializer):
    matches = MatchSerializer(many=True, source='without_finished')

    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'matches',
        )

class MatchesForPlayer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField('get_matches_filter')
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'matches',
        )
    def get_id(self,obj):
        request = self.context
        userId = request.get('userId',None)
        gameId = request.get('gameId',None)
        if userId and gameId:
            queryset = Game.objects.filter(matches__players__playerName_id=userId, games_id=gameId)
            return queryset.values_list('games_id')[0][0]
        elif userId:
            queryset = Game.objects.filter(matches__players__playerName_id=userId)
            return queryset.values_list('games_id')[0][0]


    def get_name(self,obj):
        request = self.context
        userId = request.get('userId', None)
        gameId = request.get('gameId', None)
        if userId and gameId:
            queryset = Game.objects.filter(matches__players__playerName_id=userId,games_id=gameId)
            return queryset.values_list('name')[0][0]
        elif userId:
            queryset = Game.objects.filter(matches__players__playerName_id=userId)
            return queryset.values_list('name')[0][0]


    def get_matches_filter(self,obj):
        request = self.context
        print(request)
        userId = request.get('userId', None)
        gameId = request.get('gameId', None)
        print('gameid',gameId,userId)
        if userId and gameId:
            queryset = Match.objects.filter(game__games_id=gameId,players__playerName__id=userId)
            print(queryset.values())
            return MatchSerializer(queryset,many=True).data
        elif userId:
            queryset = Match.objects.filter(players__playerName__id=userId)
            return MatchSerializer(queryset, many=True).data

