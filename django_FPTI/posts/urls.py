from django.urls import path

from . import views

urlpatterns = [
    path("homepage/", views.homepage, name="posts_home"),
    path("", views.PostListCreateView.as_view(), name="list_posts"),
    path(
        "<int:pk>/",
        views.PostRetrieveUpdateDeleteView.as_view(),
        name="post_detail",
    ),
    path("current_user/", views.get_posts_for_current_user, name="current_user"),
    path(
        "posts_for/",
        views.ListPostsForAuthor.as_view(),
        name="posts_for_current_user",
    ),
    path("test_permission/", views.only_authenticated_users_can_see_this_message, name="test_permission"),
    path("recommendations/", views.recommendations, name="recommendations"),
    path("set_score_movie/", views.setscoremovie, name="set_score_movie"),
    path("movie_details/", views.movie_details, name ="movie_details"),
    path("search/", views.search_movies, name="search_movies"),
    path("test_tensor/", views.test_load_model, name="test_load_model")
]


# djaneiro
