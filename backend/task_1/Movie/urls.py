from django.urls import path
from . import views

urlpatterns = [
    path('apiMovie/', views.MovieAPI.as_view(), name="movie_api"),
    path('apiGenre/', views.Imdb.as_view(), name="imdb_sort"),
]