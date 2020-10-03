from BoardGame import views
from django.urls import path


urlpatterns = [
    path('categorylist/',views.CategoryList.as_view(), name =views.CategoryList.name),
    path('games/',views.GameList.as_view(), name =views.GameList.name),
    path('creatematch/',views.CreateMatch.as_view(), name ='creatematch'),
    path('creatematch/',views.CreateMatchc.as_view()),
    path('register/',views.RegisterUser.as_view()),
    path('users/',views.RegisterUser.as_view()),
    path('matches/<int:pk>',views.RoomList.as_view()),
    path('allmatches',views.AllMatches.as_view()),
    path('leave-match/<int:pk>',views.PlayerDelete.as_view()),
    path('join-match/',views.PlayerJoin.as_view()),
  ]

