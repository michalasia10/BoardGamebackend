from BoardGame import views
from django.urls import path,include
from django.conf.urls import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('username', views.UserAPIView,basename='username')

urlpatterns = [
    path('categorylist/',views.CategoryList.as_view(), name =views.CategoryList.name),
    path('games/',views.GameList.as_view(), name =views.GameList.name),
    # path('register/',include(router.urls)),
    path('register/',views.UserAPIView.as_view(),name=views.UserAPIView.name),
  ]
