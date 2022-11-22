from django.urls import path

from . import views

urlpatterns = [
    path("recommendations/", views.recommendations, name="recommendations"),
    path("set_score_movie/", views.setscoremovie, name="set_score_movie"),
    path("movie_details/", views.movie_details, name ="movie_details"),
    path("search/", views.search_movies, name="serach_movies")
]
