from django.db import models

# Create your models here.



class Project(models.Model):
    projectName = models.CharField(max_length=100)

    class Meta:
        ordering = ('projectName',)

    def __str__(self):
        return self.projectName

class Game(models.Model):

    games = models.ForeignKey(Project,related_name='games',on_delete=models.CASCADE)
    name = models.CharField(max_length=144)
    playersNumber = models.IntegerField(default=2)
    imgUrl = models.URLField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class User(models.Model):

    username = models.CharField(max_length=144)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username



