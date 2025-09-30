from django.shortcuts import render
import requests 
from rest_framework.views import APIView
from rest_framework.response import Response

class TVSeries(APIView):
    def get(self,request):
        title=request.query_params.get("title")
        season=request.query_params.get("season")
        epi_no=request.query_params.get("episode_number")
        api=request.query_params.get("apikey")

        omdb_url= "https://www.omdbapi.com/"
        api_para={
            "t":title,
            "Season":season,
            "Episode":epi_no,
            "apikey":api
        }     

        response=requests.get(omdb_url,params=api_para)

        if not title:
            return Response({"Error":"Movie not found"},status=404)
        else:
            return Response(response.json())              
