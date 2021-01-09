from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save, pre_save
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
import json
import asyncio
from .models import Match
from .game_logic.tictactoe import TicTacToe

def save_post(sender, instance, **kwargs):
    chanel = get_channel_layer()
    print(chanel)
    group = instance.pk
    data = model_to_dict(instance)
    game = TicTacToe(data['state'])
    fullboard = game.check_finished()
    winner = game.run()
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    print('GROUP:', group, json_data)

    if data['status'] == 'ACTIVE':
        if str(winner) in 'XO':
            async_to_sync(chanel.group_send)(
                f'{group}',
                {
                    'type': 'winner_message',
                    'winner': winner,
                }
            )
        elif fullboard:
            async_to_sync(chanel.group_send)(
                f'{group}',
                {
                    'type': 'winner_message',
                    'winner': '',
                }
            )
        else:
            async_to_sync(chanel.group_send)(
                f'{group}',
                {'type': 'newstate', 'data': json_data}
            )


post_save.connect(save_post, sender=Match, dispatch_uid='save_post')

