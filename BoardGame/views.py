from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.reverse import reverse
from BoardGame.models import Project, Game
from BoardGame.serializers import CategorySerializer, GameSerializer


class CategoryList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class GameList(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
