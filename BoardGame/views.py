from django.shortcuts import render
from rest_framework import generics, mixins,permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from BoardGame.models import Project, Game,User
from BoardGame.serializers import CategorySerializer, GameSerializer,UserSerializer



class CategoryList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'

class UserGenericView(generics.CreateAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    name = 'register'



