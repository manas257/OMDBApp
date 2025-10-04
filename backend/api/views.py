# Simple OMDB API views for movie data
import requests
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HomeView(APIView):
    # Show the home page
    def get(self, request):
        return render(request, 'home.html')


class MovieDetailsAPI(APIView):
    # Task 1: Get movie details by title
    def get(self, request):
        # Get the movie title from URL parameters
        title = request.query_params.get('title')
        
        # Check if title was provided
        if not title:
            return Response({"error": "Need a movie title!"}, status=400)

        # Call OMDB API
        url = "https://www.omdbapi.com/"
        params = {"t": title, "apikey": settings.OMDB_API_KEY}

        try:
            response = requests.get(url, params=params)
            data = response.json()

            # Check if movie was found
            if data.get("Response") == "False":
                return Response({"error": "Movie not found"}, status=404)
            
            # Return only the fields we need
            result = {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "plot": data.get("Plot"),
                "country": data.get("Country"),
                "awards": data.get("Awards"),
                "director": data.get("Director"),
                "ratings": data.get("Ratings", [])
            }
            
            return Response(result)
            
        except:
            return Response({"error": "Something went wrong"}, status=500)


class TVEpisodeAPI(APIView):
    # Task 2: Get TV episode details
    def get(self, request):
        # Get parameters from URL
        series_title = request.query_params.get('series_title')
        season = request.query_params.get('season')
        episode_number = request.query_params.get('episode_number')

        # Check if all required parameters are provided
        if not series_title:
            return Response({"error": "Need series_title!"}, status=400)
        if not season:
            return Response({"error": "Need season number!"}, status=400)
        if not episode_number:
            return Response({"error": "Need episode_number!"}, status=400)

        # Call OMDB API for episode
        url = "https://www.omdbapi.com/"
        params = {
            "t": series_title,
            "Season": season,
            "Episode": episode_number,
            "apikey": settings.OMDB_API_KEY
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("Response") == "False":
                return Response({"error": "Episode not found"}, status=404)
            
            # Return episode info
            result = {
                "series_title": series_title,
                "season": data.get("Season"),
                "episode": data.get("Episode"),
                "episode_title": data.get("Title"),
                "plot": data.get("Plot"),
                "released": data.get("Released"),
                "runtime": data.get("Runtime"),
                "director": data.get("Director"),
                "writer": data.get("Writer"),
                "actors": data.get("Actors"),
                "imdb_rating": data.get("imdbRating"),
                "imdb_id": data.get("imdbID")
            }
            
            return Response(result)
            
        except:
            return Response({"error": "Something went wrong"}, status=500)


class GenreMoviesAPI(APIView):
    # Task 3: Get top movies by genre
    def get(self, request):
        genre = request.query_params.get('genre')
        
        if not genre:
            return Response({"error": "Need a genre!"}, status=400)

        try:
            movies = self.find_movies_by_genre(genre.capitalize())
            
            if not movies:
                return Response({"error": f"No {genre} movies found"}, status=404)
            
            # Sort movies by rating (highest first) and get top 15
            movies.sort(key=lambda x: float(x["imdb_rating"]) if x["imdb_rating"] != "N/A" else 0, reverse=True)
            top_movies = movies[:15]
            
            return Response({
                "genre": genre.capitalize(),
                "total_found": len(movies),
                "top_movies": top_movies
            })
            
        except:
            return Response({"error": "Something went wrong"}, status=500)

    def find_movies_by_genre(self, genre):
        # Search for movies and collect them
        url = "https://www.omdbapi.com/"
        movies = []
        page = 1
        
        # Search through a few pages to get enough movies
        while len(movies) < 50 and page <= 5:
            search_params = {
                "apikey": settings.OMDB_API_KEY,
                "s": genre,
                "type": "movie",
                "page": page
            }
            
            try:
                search_response = requests.get(url, params=search_params)
                search_data = search_response.json()
                
                if search_data.get("Response") == "False":
                    break
                
                search_results = search_data.get("Search", [])
                if not search_results:
                    break
                
                # Get details for each movie
                for movie in search_results:
                    detail_params = {
                        "apikey": settings.OMDB_API_KEY,
                        "i": movie["imdbID"]
                    }
                    
                    detail_response = requests.get(url, params=detail_params)
                    detail_data = detail_response.json()
                    
                    # Check if this movie actually has our genre
                    movie_genres = detail_data.get("Genre", "")
                    if genre.lower() in movie_genres.lower():
                        movies.append({
                            "title": detail_data.get("Title"),
                            "year": detail_data.get("Year"),
                            "imdb_rating": detail_data.get("imdbRating", "N/A"),
                            "genre": detail_data.get("Genre"),
                            "director": detail_data.get("Director"),
                            "plot": detail_data.get("Plot"),
                            "imdb_id": detail_data.get("imdbID")
                        })
                    
                    if len(movies) >= 50:
                        break
                        
                page += 1
                
            except:
                break
        
        return movies