from django.http import JsonResponse
from rest_framework import generics, mixins,permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from BoardGame.models import Project, Game,Usernames
from BoardGame.serializers import CategorySerializer, GameSerializer,UserSerializer
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
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


@parser_classes((JSONParser,FormParser, MultiPartParser))
class UserAPIView(APIView):
    # parser_classes = [JSONParser,]
    name = 'register'
    def get(self,request):
        users = Usernames.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(request.body)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class UserAPIView(GenericViewSet,  # generic view functionality
#                      CreateModelMixin,  # handles POSTs
#                      RetrieveModelMixin,  # handles GETs for 1 Company
#                      UpdateModelMixin,  # handles PUTs and PATCHes
#                      ListModelMixin):  # handles GETs for many Companies
#     serializer_class = UserSerializer
#     queryset = Usernames.objects.all()
#     lookup_field = 'id'
#
#     def get(self, request, id=None):
#
#         if id:
#             return self.retrieve(request)
#
#         else:
#             return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#     def put(self, request, id=None):
#         return self.update(request, id)