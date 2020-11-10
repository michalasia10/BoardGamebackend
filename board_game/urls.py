from .views import CategoryList,GameList,CreateMatch,RegisterUser,RoomList,AllMatches,PlayerDelete,PlayerJoin,RoomDetail
from django.urls import path


urlpatterns = [
    path('categorylist/',CategoryList.as_view(), name =CategoryList.name),
    path('games/',GameList.as_view(), name =GameList.name),
    path('creatematch/',CreateMatch.as_view(), name ='creatematch'),
    path('register/',RegisterUser.as_view()),
    path('users/',RegisterUser.as_view()),
    path('matches/<int:pk>',RoomList.as_view()),
    path('allmatches',AllMatches.as_view()),
    path('leave-match/<int:pk>',PlayerDelete.as_view()),
    path('join-match/',PlayerJoin.as_view()),
    path('roomdetail/<int:pk>',RoomDetail.as_view())
  ]

