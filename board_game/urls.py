from .views import CategoryList, GameList, CreateMatch, RegisterUser,  PlayerDelete, PlayerJoin,RoomDetail
# MatchesUnFinshed,RoomList, AllMatches,
from django.urls import path, include

urlpatterns = [
    path('',include('board_game.match_history.urls')),
    path('categorylist/', CategoryList.as_view(), name=CategoryList.name),
    path('games/', GameList.as_view(), name=GameList.name),
    path('creatematch/', CreateMatch.as_view(), name='creatematch'),
    path('register/', RegisterUser.as_view(),name='register'),
    path('users/', RegisterUser.as_view()),
    # path('matches/<int:pk>', MatchesUnFinshed.as_view(),name='matches'),
    # path('match-history/<int:pk>', RoomList.as_view(),name='match-history'),
    # path('allmatches', AllMatches.as_view(), name='allmatches'),
    path('leave-match/<int:pk>', PlayerDelete.as_view(), name='leave-match'),
    path('join-match/', PlayerJoin.as_view(),name='join-match'),
    path('roomdetail/<int:pk>', RoomDetail.as_view(),name='roomdetail')
]


