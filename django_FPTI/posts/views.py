from accounts.serializers import CurrentUserPostsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Post, User
from .serializers import PostSerializer
from .permissions import ReadOnly, AuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
import json
import csv
import datetime


class CustomPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"


def BoboSort(lista, criterio,qtd):
    saida = []
    k=0;
    while((len(saida)<qtd) and k<len(lista)):
        max = -100.0;
        for i,item in enumerate(lista):
            if criterio in item:
                if ',' in item[criterio]:
                    item[criterio] = item[criterio].replace(',',"")
                if(float(item[criterio]) > max):
                    max = float(item[criterio])
                    selecionado = item;
                    apagar = i;
        lista.pop(apagar)
        saida.append(selecionado);
        k=k+1;
    return saida


def Ordena(arquivo, crit, saida,qtd):
    file = open(arquivo);
    movies = json.load(file);
    with open(saida, 'w', encoding='utf-8') as f:
        json.dump(BoboSort(movies, crit, qtd), f, ensure_ascii=False, indent=4)
    file.close()


@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAuthenticated])
def recommendations(request: Request):


    f = open("successData.json")
    Ordena("successData.json", "imdbScore", 'Top20Score.json',20);
    Ordena("successData.json", "popularity", 'Top20pop.json',20);
   
    g = open("Top20Score.json")
    h = open("Top20pop.json")

    movies = json.load(f)
    f.close()
    bests = []

    best_20 = json.load(g)
    g.close()
    movie_dict = dict()
    movie_dict["recName"] = "Top Score 20"
    movie_dict["recList"] = best_20

    bests.append(movie_dict)


    best_20 =  json.load(h)
    h.close()
    
    movie_dict = dict()
    movie_dict["recName"] = "Top Popularity 20"
    movie_dict["recList"] = best_20

    bests.append(movie_dict)

    best_20 = []

    user = request.user

    liked = user.liked_movies

    liked = liked.split(",")

    for movie in movies:
        if movie["id"] in liked:
            
            best_20.append(movie)
        
        if len(best_20) > 20:
            break
    
    movie_dict = dict()
    movie_dict["recName"] = "Liked Movies"
    movie_dict["recList"] = best_20

    bests.append(movie_dict)

    if user.predicts != "":

        recs_movies_infos = []

        predicts = user.predicts
        predicts = predicts.split(",")

        for movie in movies:
            if movie["id"] in predicts:
                recs_movies_infos.append(movie)

    else:
        liked_all_users = User.objects.values_list("liked_movies")

        recs = []

        
        for movie_liked in liked:
            counter = 0
            for item in liked_all_users:
                l_item = item[0].split(",")

                if movie_liked in l_item:
                    counter += 1
                    if counter == 3:
                        for id_item in l_item:
                            recs.append(id_item)
            
        recs_tratada = []

        for movie_rec in recs:
            if movie_rec not in recs_tratada and movie_rec not in liked:
                recs_tratada.append(movie_rec)

        
        recs_movies_infos = []

        for movie in movies:
            if movie["id"] in recs_tratada:
                recs_movies_infos.append(movie)


    movie_dict = dict()
    movie_dict["recName"] = "Recommendations"
    movie_dict["recList"] = recs_movies_infos

    bests.append(movie_dict)

    response = bests

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=["PUT"])
@permission_classes([IsAuthenticated])
def setscoremovie(request: Request):

    ct = str(datetime.datetime.now())

    movieId = request.data.get("movieId")

    score = request.data.get("score")
 
    user = request.user

    liked = user.liked_movies
    disliked = user.disliked_movies

    timestamp_liked = user.timestamp_liked_movies
    timestamp_disliked = user.timestamp_disliked_movies

    if score == "like":

        # Adiciona no like
        if liked == '':
            string_back_likes = movieId
            string_back_likes_times = ct
        else:
            liked = liked.split(",")
            timestamp_liked = timestamp_liked.split(",")

            if movieId not in liked:
                liked.append(movieId)
                timestamp_liked.append(ct)

            if len(liked) > 0:
                string_back_likes = "" + liked[0]
                string_back_likes_times = "" + timestamp_liked[0]
            else:
                string_back_likes = ""
                string_back_likes_times = ""

            for i in range(1, len(liked)):

                string_back_likes = string_back_likes + "," + liked[i]
                string_back_likes_times = string_back_likes_times + "," + timestamp_liked[i]
        
        # Remove no dislike
        disliked = disliked.split(",")
        timestamp_disliked = timestamp_disliked.split(",")

        if movieId in disliked:
            new_disliked = []
            new_times_disliked = []

            for i in range(len(disliked)):
                if disliked[i] != movieId:
                    new_disliked.append(disliked[i])
                    new_times_disliked.append(timestamp_disliked[i])
        
            disliked = new_disliked
            timestamp_disliked = new_times_disliked

        if len(disliked) > 0 :
            string_back_dislikes = "" + disliked[0]
            string_back_dislikes_times = "" + timestamp_disliked[0]
        else:
            string_back_dislikes = ""
            string_back_dislikes_times = ""

        for i in range(1, len(disliked)):

            string_back_dislikes = string_back_dislikes + "," + disliked[i]
            string_back_dislikes_times = string_back_dislikes_times + "," + timestamp_disliked[i]
    
    elif score == "dislike":

        # Adiciona no dislike
        if disliked == '':
            string_back_dislikes = movieId
            string_back_dislikes_times = ct
        else:
            disliked = disliked.split(",")
            timestamp_disliked = timestamp_disliked.split(",")

            if movieId not in disliked:
                disliked.append(movieId)
                timestamp_disliked.append(ct)

            if len(disliked) > 0 :
                string_back_dislikes = "" + disliked[0]
                string_back_dislikes_times = "" + timestamp_disliked[0]
            else:
                string_back_dislikes = ""

            for i in range(1, len(disliked)):

                string_back_dislikes = string_back_dislikes + "," + disliked[i]
                string_back_dislikes_times = string_back_dislikes_times + "," + timestamp_disliked[i]
        
        # Remove do like
        liked = liked.split(",")
        timestamp_liked = timestamp_liked.split(",")

        if movieId in liked:
            new_liked = []
            new_times_liked = []

            for i in range(len(liked)):
                if liked[i] != movieId:
                    new_liked.append(liked[i])
                    new_times_liked.append(timestamp_liked[i])
        
            liked = new_liked
            timestamp_liked = new_times_liked

        if len(liked) > 0:
            string_back_likes = "" + liked[0]
            string_back_likes_times = "" + timestamp_liked[0]
        else:
            string_back_likes = ""
            string_back_likes_times = ""

        for i in range(1, len(liked)):

            string_back_likes = string_back_likes + "," + liked[i]
            string_back_likes_times = string_back_likes_times + "," + timestamp_liked[i]

    else:
        

        # Remove no dislike
        disliked = disliked.split(",")
        timestamp_disliked = timestamp_disliked.split(",")

        if movieId in disliked:
            new_disliked = []
            new_times_disliked = []

            for i in range(len(disliked)):
                if disliked[i] != movieId:
                    new_disliked.append(disliked[i])
                    new_times_disliked.append(timestamp_disliked[i])
        
            disliked = new_disliked
            timestamp_disliked = new_times_disliked

        if len(disliked) > 0 :
            string_back_dislikes = "" + disliked[0]
            string_back_dislikes_times = "" + timestamp_disliked[0]
        else:
            string_back_dislikes = ""
            string_back_dislikes_times = ""

        for i in range(1, len(disliked)):

            string_back_dislikes = string_back_dislikes + "," + disliked[i]
            string_back_dislikes_times = string_back_dislikes_times + "," + timestamp_disliked[i]
        
        # Remove do like
        liked = liked.split(",")
        timestamp_liked = timestamp_liked.split(",")

        if movieId in liked:
            new_liked = []
            new_times_liked = []

            for i in range(len(liked)):
                if liked[i] != movieId:
                    new_liked.append(liked[i])
                    new_times_liked.append(timestamp_liked[i])
        
            liked = new_liked
            timestamp_liked = new_times_liked

        if len(liked) > 0:
            string_back_likes = "" + liked[0]
            string_back_likes_times = "" + timestamp_disliked[0]
        else:
            string_back_likes = ""
            string_back_likes_times = ""

        for i in range(1, len(liked)):

            string_back_likes = string_back_likes + "," + liked[i]
            string_back_likes_times = string_back_likes_times + "," + timestamp_liked[i]

        
    
    user.liked_movies = string_back_likes
    user.disliked_movies = string_back_dislikes
    user.timestamp_liked_movies = string_back_likes_times
    user.timestamp_disliked_movies = string_back_dislikes_times

    user.save()
    response = { "status": "Succesful"}

    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def movie_details(request: Request):


    user = request.user

    liked = user.liked_movies
    disliked = user.disliked_movies

    movieId = request.query_params.get("movieId")

    f = open("successData.json")
    movies = json.load(f)

    move_found = {"message": "N??o encontrado"}

    for movie in movies:
        if movie["id"] == movieId:
            move_found = movie
            if move_found["id"] in liked:
                move_found["score"] = "like"
            elif move_found["id"] in disliked:
                move_found["score"] = "dislike"
            else:
                move_found["score"] = "unscore"
        
            return Response(data=move_found, status=status.HTTP_200_OK)

    return Response(data=move_found, status=status.HTTP_404_NOT_FOUND)

@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def search_movies(request: Request):

    key = request.data.get("keySearch")

    f = open("successData.json")
    movies = json.load(f)

    movies_found = []

    for movie in movies:
        if key.lower() in movie["title"].lower():
            movies_found.append(movie)

    return Response(data=movies_found, status=status.HTTP_200_OK)