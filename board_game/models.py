from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
import json


# Create your models here.


class Project(models.Model):
    projectName = models.CharField(max_length=100)

    class Meta:
        ordering = ('projectName',)

    def __str__(self):
        return self.projectName


class Game(models.Model):
    games = models.ForeignKey(Project, related_name='games', on_delete=models.CASCADE)
    name = models.CharField(max_length=144)
    imgUrl = models.URLField(max_length=400)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)


class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='matches')
    maxPlayers = models.IntegerField(default=2)
    state = models.CharField(max_length=144,default='---------')

    class Meta:
        ordering = ('game',)

    def __str__(self):
        return str(self.game)


def save_post(sender, instance, **kwargs):
    chanel = get_channel_layer()
    group = instance.pk
    data = model_to_dict(instance)
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    async_to_sync(chanel.group_send)(
        f'{group}',
        {'type': 'newstate', 'data': json_data}
    )


post_save.connect(save_post, sender=Match, dispatch_uid='save_post')


class User(models.Model):
    username = models.CharField(max_length=144, blank=False, unique=True)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return str(self.username)


class Player(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE,related_name='players')
    playerName = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True)

    class Meta:
        ordering = ('playerName',)

    def __str__(self):
        return str(self.playerName)
