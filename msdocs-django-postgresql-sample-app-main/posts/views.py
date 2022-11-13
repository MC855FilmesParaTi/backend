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


class CustomPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def homepage(request: Request):

    if request.method == "POST":
        data = request.data

        f = open("test.txt", "r")

        msg = f.readline()

        response = {"message": msg, "data": data}

        return Response(data=response, status=status.HTTP_201_CREATED)
    
    f = open('test.txt', "r")

    msg = f.readline()

    response = {"message": msg}
    return Response(data=response, status=status.HTTP_200_OK)


class PostListCreateView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):

    """
    a view for creating and listing posts
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPaginator
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AuthorOrReadOnly]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserPostsSerializer(instance=user, context={"request": request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username") or None

        queryset = Post.objects.all()

        if username is not None:
            return Post.objects.filter(author__username=username)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAuthenticated])
def only_authenticated_users_can_see_this_message(request: Request):

    f = open('test.txt', "r")

    msg = f.readline()

    data = request.data

    param_id = request.query_params.get("movieId")

    print(param_id)

    response = {"message": msg, "data": data, "param_id": param_id}
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAuthenticated])
def recommendations(request: Request):
    username = request.query_params.get("username")

    f = open("successData.json")

    movies = json.load(f)

    bests = []

    best_20 = []
    
    for movie in movies:
        if float(movie["imdbScore"]) > 8.0:
            
            best_20.append(movie)
        
        if len(best_20) > 20:
            break
    
    movie_dict = dict()
    movie_dict["recName"] = "Top Score 20"
    movie_dict["recList"] = best_20

    bests.append(movie_dict)


    best_20 = []
    
    for movie in movies:
        if "popularity" in movie:
            if ',' in movie["popularity"]:
                movie["popularity"] = movie["popularity"].replace(',',"")

            if int(movie["popularity"]) > 600:
                
                best_20.append(movie)
            
            if len(best_20) > 20:
                break
    
    movie_dict = dict()
    movie_dict["recName"] = "Top Popularity 20"
    movie_dict["recList"] = best_20

    bests.append(movie_dict)

    best_20 = []

    user = User.objects.get(username=username)

    value = user.liked_movies

    value = value.split(",")

    for movie in movies:
        if movie["id"] in value:
            
            best_20.append(movie)
        
        if len(best_20) > 20:
            break
    
    movie_dict = dict()
    movie_dict["recName"] = "Liked Movies"
    movie_dict["recList"] = best_20

    bests.append(movie_dict)

    response = bests

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def setlikemovie(request: Request):

    if request.method == "POST":

        username = request.data.get("username")

        movieId = request.data.get("movieId")

        user = User.objects.get(username=username)

        value = user.liked_movies

        if value == '':
            string_back = movieId
        else:
            value = value.split(",")

            if movieId not in value:
                value.append(movieId)

            string_back = "" + value[0]


            for i in range(1, len(value)):

                string_back = string_back + "," + value[i]

        
        user.liked_movies = string_back

        user.save()
        response = { "status": "Succesful"}

        return Response(data=response, status=status.HTTP_200_OK)
    
    elif request.method == "DELETE":

        username = request.data.get("username")

        movieId = request.data.get("movieId")

        user = User.objects.get(username=username)

        value = user.liked_movies

  
        value = value.split(",")

        if movieId in value:
            value.remove(movieId)

        string_back = "" + value[0]


        for i in range(1, len(value)):

            string_back = string_back + "," + value[i]

        
        user.liked_movies = string_back

        user.save()
        response = { "status": "Succesful"}

        return Response(data=response, status=status.HTTP_200_OK)
