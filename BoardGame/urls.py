from BoardGame import views
from django.urls import path

urlpatterns = [
    path('categorylist/',views.CategoryList.as_view(), name =views.CategoryList.name),
    path('gamelist/',views.GameList.as_view(), name =views.GameList.name)
]