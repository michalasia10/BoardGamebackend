from BoardGame import views
from django.urls import path
from django.conf.urls import static
from django.conf import settings



urlpatterns = [
    path('categorylist/',views.CategoryList.as_view(), name =views.CategoryList.name),
    path('games/',views.GameList.as_view(), name =views.GameList.name),
    path('register/',views.UserAPIView.as_view(),name = views.UserAPIView.name),
  ]
