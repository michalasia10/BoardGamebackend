from django.http import JsonResponse
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from BoardGame.models import Project, Game, Usernames
from BoardGame.serializers import CategorySerializer, GameSerializer, UserSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
import json


class CategoryList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


# @parser_classes((JSONParser,FormParser, MultiPartParser))
class UserAPIView(APIView):
    # parser_classes = [JSONParser,]
    name = 'register'

    def get(self, request):
        users = Usernames.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request,*args,**kwargs):
        serializer = UserSerializer(data=request.data.get('username'))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class UserAPIView(generics.CreateAPIView):
#     queryset = Usernames.objects.all()
#     serializer_class = UserSerializer
#     name = 'register'
#     #permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(username=self.request.username)
