from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
import json
import asyncio

# Create your models here.


class Project(models.Model):
    projectName = models.CharField(max_length=100,
                                   help_text='Category of games',
                                   verbose_name='game category')

    class Meta:
        ordering = ('projectName',)

    def __str__(self):
        return self.projectName


class Game(models.Model):
    games = models.ForeignKey(Project, related_name='games',
                              on_delete=models.CASCADE,
                              help_text='Category of game which belong to',
                              verbose_name='game category')
    name = models.CharField(max_length=144,
                            help_text='Game name',
                            verbose_name='game name')
    imgUrl = models.URLField(max_length=400,
                             help_text='URL to game image for logo',
                             verbose_name='game\'s logo url')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)


class Match(models.Model):
    class StatusInGame(models.TextChoices):
        CREATED = 'CREATED', 'CREATED'
        ACTIVE = 'ACTIVE', 'ACTIVE'
        FINISHED = 'FINISHED','FINISHED'
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name='matches',
                             help_text='Type of game which match belong to',
                             verbose_name='type of game')
    maxPlayers = models.IntegerField(default=2,
                                     help_text='Number of max players in each game',
                                     verbose_name='max players in game')
    state = models.CharField(max_length=144, default='---------',
                             help_text='State of board',
                             verbose_name='state of board')
    status = models.CharField(max_length=144,choices=StatusInGame.choices, default=StatusInGame.CREATED)

    class Meta:
        ordering = ('game',)

    def __str__(self):
        return str(self.game)


# def save_post(sender, instance, **kwargs):
#     chanel = get_channel_layer()
#     print(chanel)
#     group = instance.pk
#     data = model_to_dict(instance)
#     json_data = json.dumps(data, cls=DjangoJSONEncoder)
#     print('GROUP:',group,json_data)
#
#     async_to_sync(chanel.group_send)(
#         f'{group}',
#         {'type': 'newstate', 'data': json_data}
#     )
#
#
#
# post_save.connect(save_post, sender=Match, dispatch_uid='save_post')


class User(models.Model):
    username = models.CharField(max_length=144, blank=False, unique=True)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return str(self.username)


class Player(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE,
                              related_name='players',
                              help_text='choose match/room u want to join',
                              verbose_name='match/room')
    playerName = models.OneToOneField(User, on_delete=models.CASCADE,
                                      unique=True,
                                      primary_key=True,
                                      help_text='user will be a player ',
                                      verbose_name='player',)


    class Meta:
        ordering = ('playerName',)

    def __str__(self):
        return str(self.playerName)
