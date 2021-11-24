from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Movie, Actor, Review, Comment
from .serializers.movie import MovieListSerializer, MovieSerializer
from .serializers.review import ReviewListSerializer, ReviewSerializer, ReviewViewSerializer


User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review_create_or_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        reviews = movie.reviews.order_by('-pk')
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.user and request.user.is_authenticated:
        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(movie=movie)
                return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def review_detail_or_update_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewViewSerializer(review)
        return Response(serializer.data)

    elif request.user and request.user.is_authenticated:
        if request.method == 'PUT':
            serializer = ReviewSerializer(data=request.data, instance=review)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            review.delete()
            return Response('Delete success', status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def review_likes(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)

    data = {
        'like_count': len(review.like_users.all()),
        'is_liked': review.like_users.filter(pk=request.user.pk).exists()
    }

    return Response(data)



# @api_view(['GET', 'POST'])
# def review_comment_create_or_list(request, review_pk):
#     review = get_object_or_404(Review, pk=review_pk)
#
#     if request.method == 'GET':
#         comments = review.comments.all()
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#
#     else:
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(review=review)
#             return Response(serializer.data)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def review_comment_detail_or_update_delete(request, review_pk, comment_pk):
#     review = get_object_or_404(Review, pk=review_pk)
#     comment = get_object_or_404(Comment, pk=comment_pk)
#
#     if request.method == 'GET':
#         serializer = CommentSerializer(review)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = CommentSerializer(data=request.data, instance=comment)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#     else:
#         review.delete()
#         return Response('Delete success', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
# TODO: 가입한 유저만 볼 수 있도록 변경
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def recommendations_by_followings(request):
    # TODO: request.user로 변경
    target_user = User.objects.get(id=78)

    followings = target_user.profile.followings.all()
    my_reviews = target_user.movies_review.all()

    recommend_list = []

    for following in followings:
        recommendations = []
        for review in following.user.movies_review.filter(rank__gte=8):
            if not my_reviews.filter(movie=review.movie).exists():
                recommendations.append({
                    'movie': review.movie.id,
                    'rank': review.rank,
                })
        recommend_list.append({
            'target_user_id': following.user.id,
            'recommendations': recommendations,
        })

    return Response(recommend_list)


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def recommendations_by_actors(request):
    target_user = User.objects.get(id=78)
    my_reviews = target_user.movies_review.filter(rank__gte=8)
    recommend_list = []

    for review in my_reviews:
        target_movie = review.movie.id
        recommends = []

        for actor in review.movie.actors.all():
            result_movies = actor.movies.filter(~Q(id=target_movie))
            movie_list = []
            for result_movie in result_movies:
                if not target_user.movies_review.filter(movie=result_movie.id).exists():
                    movie_list.append(result_movie.id)

            if movie_list:
                recommends.append({
                    'actor': actor.id,
                    'movies': movie_list
                })
        recommend_list.append({
            'target_movie': target_movie,
            'rank': review.rank,
            'recommendations': recommends,
        })

    return Response(recommend_list)


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def recommendations_by_movies(request):
    target_user = User.objects.get(id=78)
    my_reviews = target_user.movies_review.filter(rank__gte=8)
    recommend_list = []

    for review in my_reviews:
        target_movie = review.movie.id
        recommendations = []

        for movie in review.movie.recommendations:
            if Movie.objects.filter(id=movie).exists():
                if not target_user.movies_review.filter(id=movie).exists():
                    recommendations.append(movie)

        recommend_list.append({
            'target_movie': target_movie,
            'rank': review.rank,
            'recommendations': recommendations,
        })

    return Response(recommend_list)
