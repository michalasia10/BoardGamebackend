from rest_framework import serializers
from board_game.models import  Game, Match
from board_game.serializers import MatchSerializer


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
