from board_game.serializers import RoomSerializerWithAllStates, RoomSerializerWithoutFinished,MatchesForPlayer
from django.shortcuts import get_object_or_404
from board_game.models import Game
from dataclasses import dataclass

SERIALIZER_METHODS = {
    0: {
        "serializer": RoomSerializerWithAllStates,
        "kwargs": {
            'many': True
        }
    },
    1: {
        'gameId': RoomSerializerWithoutFinished,
        'userId': {
            "serializer": MatchesForPlayer,
            "kwargs": {
                "many": False
            },
        }
    },
    2: {
        "serializer": MatchesForPlayer,
        "kwargs": {
            'many': False
        }
    }
}


@dataclass()
class OptionalSerializer:
    request : dict

    def create_data(self,serializer, context: dict):
        if 'gameId' in context.keys() and not 'userId' in context.keys():
            game = get_object_or_404(Game, pk=context['gameId'])
            data = serializer(game).data
            return data
        else:
            extra_kwargs = serializer['kwargs']
            serializer = serializer['serializer']
            game = Game.objects.all()
            data = serializer(game, context=context, **extra_kwargs).data
            return data


    def check_number_of_keys(self):
        request = self.request
        if len(request.keys()) % 2 == 0:
            serializer = SERIALIZER_METHODS[len(request.keys())]
            context = request
            return self.create_data(serializer, context)
        else:
            key = list(request.keys())[0]
            serializer = SERIALIZER_METHODS[1][key]
            context = request
            return self.create_data(serializer, context)
