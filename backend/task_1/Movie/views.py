from django.shortcuts import render
import requests 
from rest_framework.views import APIView
from rest_framework.response import Response

class MovieAPI(APIView):
    def get(self,request):
        title=request.query_params.get("title")
        api=request.query_params.get("apikey")

        omdb_url="https://www.omdbapi.com/"
        api_para={
            "t":title,
            "apikey":api
        }

        response=requests.get(omdb_url,params=api_para)

        if response.get("Response")=="False":
            return Response({"Error":"Movie not found"},status=404)
        else:
            return Response(response.json())
        
class Imdb(APIView):
    def get(self,request):
        genre=request.query_params.get("genre")
        api=request.query_params.get("apikey")

        omdb_url="https://www.omdbapi.com/"
        genre=genre.capitalize()
        Movies=[]
        pg=1
        count=15    
        api_para={
            "apikey":api,
            "s":genre,
            "type":"movie",
            "page":pg
        }
        
        while len(Movies)<15:
            movie_search=requests.get(omdb_url, params=api_para).json()
            movie=movie_search.get("Search")

            for i in movie:
                movie_detail=requests.get(omdb_url,params={"apikey":api,"i":i["imdbID"]}).json()
                if genre in movie_detail.get("Genre"):
                    Movies.append({"title":movie_detail.get("Title"),"imdb_rating":movie_detail.get("imdbRating"),"genre":movie_detail.get("Genre")})
                    if len(Movies)>=15:
                      break
            pg+=1
        
        Movies.sort(key=lambda x: x["imdb_rating"], reverse=True)

        return Response({"movies":Movies})

