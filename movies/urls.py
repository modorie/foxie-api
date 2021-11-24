from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:movie_pk>/', views.movie_detail),

    path('movies/<int:movie_pk>/reviews/', views.review_create_or_list),
    path('movies/<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail_or_update_delete),
    path('movies/<int:movie_pk>/reviews/<int:review_pk>/likes/', views.review_likes),

    # path('movies/<int:movie_pk>/reviews/<int:review_pk>/comments/', views.review_comment_create_or_list),
    # path('movies/<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/', views.review_comment_detail_or_update_delete),

    path('movies/recommendations/followings', views.recommendations_by_followings),
    path('movies/recommendations/actors', views.recommendations_by_actors),
    path('movies/recommendations/movies', views.recommendations_by_movies),
    ]
