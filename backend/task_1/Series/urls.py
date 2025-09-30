from django.urls import path
from . import views

urlpatterns = [
    path('apiTV/', views.TVSeries.as_view(), name=" TVSeries_api"),
]