# URL routes for our movie API
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('movie/', views.MovieDetailsAPI.as_view(), name='movie_details'),
    path('episode/', views.TVEpisodeAPI.as_view(), name='tv_episode'),
    path('movies/genre/', views.GenreMoviesAPI.as_view(), name='genre_movies'),
]