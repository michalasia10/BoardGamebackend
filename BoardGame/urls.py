from BoardGame import views
from django.urls import path


urlpatterns = [
    path('categorylist/',views.CategoryList.as_view(), name =views.CategoryList.name),
    path('games/',views.GameList.as_view(), name =views.GameList.name),
    path('creatematch/',views.CreateMatch.as_view(), name ='creatematch'),
    path('register/',views.UserAPIView.as_view(),name=views.UserAPIView.name),
    path('matches/',views.RoomList.as_view(),name='matches'),
    path('leave-match/<int:pk>',views.PlayerDelete.as_view()),
    path('join-match/<int:matchID/<int:userID>',views.PlayerDelete.as_view()),
    # path('creatematch/',views.UserAPIView.as_view(),name=views.UserAPIView.name),
  ]

