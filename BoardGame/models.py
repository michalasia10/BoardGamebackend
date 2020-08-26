from django.db import models


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
    playersNumber = models.IntegerField(default=2)
    imgUrl = models.URLField(max_length=400)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Match(models.Model):
    roomName = models.CharField(max_length=140, default='room',unique=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE,related_name='rooms')

    class Meta:
        ordering = ('roomName',)



class User(models.Model):
    username = models.CharField(max_length=144, blank=False, unique=True)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


class Player(models.Model):
    room = models.ForeignKey(Match,on_delete=models.CASCADE)
    playerName = models.OneToOneField(User, on_delete=models.CASCADE, unique=True,primary_key=True)

    class Meta:
        ordering = ('playerName',)



