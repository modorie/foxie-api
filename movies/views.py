from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q, Count

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

import re
import random

from .models import Movie, Actor, Review, Comment
from .serializers.movie import MovieListSerializer, MovieSerializer
from .serializers.review import (
    ReviewListSerializer, ReviewSerializer, ReviewViewSerializer,
    CommentSerializer, CommentViewSerializer,
)


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


@api_view(['GET'])
@permission_classes([AllowAny])
def review_feed_new(request):
    reviews = Review.objects.order_by('-pk')[:50]
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def review_feed_popular(request):
    reviews = Review.objects.all().annotate(likes=Count('like_users')).order_by('-likes')[:50]
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def review_feed_followings(request):
    reviews = Review.objects.filter(author_id__in=request.user.profile.followings.values('user_id'))
    serializer = ReviewSerializer(reviews, many=True)
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


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review_comment_create_or_list(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        comments = review.comments.all()
        serializer = CommentViewSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.user and request.user.is_authenticated:
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def review_comment_detail_or_update_delete(request, movie_pk, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentViewSerializer(comment)
        return Response(serializer.data)

    elif request.user and request.user.is_authenticated:
        if request.method == 'PUT':
            serializer = CommentSerializer(data=request.data, instance=comment)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        elif request.method == 'DELETE':
            comment.delete()
            return Response('Delete success', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def recommendations_by_followings(request):
    target_user = User.objects.get(id=request.user.id)

    followings = target_user.profile.followings.all()
    my_reviews = target_user.movies_review.all()

    recommend_list = []

    for following in followings:
        recommendations = []
        for review in following.user.movies_review.filter(rank__gte=8):
            if not my_reviews.filter(movie=review.movie).exists():
                recommendations.append(review.movie.id)
        if recommendations:
            recommend_list.append({
                'type': 'followings',
                'target_user': {
                    'id': following.user.id,
                    'username': following.user.username,
                    'nickname': following.user.profile.nickname,
                },
                'recommendation': random.choice(recommendations),
            })

    return Response(random.choice(recommend_list))


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def recommendations_by_actors(request):
    target_user = User.objects.get(id=request.user.id)
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
                korean_name = ''

                for name in actor.also_known_as:
                    if re.match("[가-힣]+", str(name)):
                        korean_name = name

                recommends.append({
                    'actor': {
                        'id': actor.id,
                        'name': actor.name,
                        'korean_name': korean_name,
                    },
                    'movie': random.choice(movie_list)
                })
        recommend_list.append({
            'type': 'actors',
            'target_movie': {
                'id': target_movie,
                'title': review.movie.title,
            },
            'rank': review.rank,
            'recommendation': random.choice(recommends),
        })
    return Response(random.choice(recommend_list))


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def recommendations_by_movies(request):
    target_user = User.objects.get(id=request.user.id)
    my_reviews = target_user.movies_review.filter(rank__gte=8)
    recommend_list = []

    for review in my_reviews:
        target_movie = review.movie.id
        recommendations = []

        for movie in review.movie.recommendations:
            if Movie.objects.filter(id=movie).exists():
                if not target_user.movies_review.filter(id=movie).exists():
                    recommendations.append(movie)

        if recommendations:
            recommend_list.append({
                'type': 'movies',
                'target_movie': {
                    'id': target_movie,
                    'title': review.movie.title,
                },
                'rank': review.rank,
                'recommendation': random.choice(recommendations),
            })

    return Response(random.choice(recommend_list))


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def recommendations_preview(request):
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

        if recommendations:
            recommend_list.append({
                'type': 'movies',
                'target_movie': {
                    'id': target_movie,
                    'title': review.movie.title,
                },
                'rank': review.rank,
                'recommendation': random.choice(recommendations),
            })

    return Response(random.choice(recommend_list))