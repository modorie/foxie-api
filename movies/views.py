from django.http import response
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Actor, Director, Movie, Review, Comment

from .serializers.actor import ActorSerializer
from .serializers.director import DirectorSerializer
from .serializers.movie import MovieSerializer, MovieListSerializer
from .serializers.review import ReviewSerializer, ReviewListSerializer, CommentSerializer


# @api_view(['GET'])
# def actor_detail(request, actor_pk):
#     actor = get_object_or_404(Actor, pk=actor_pk)
#     actor = Actor.objects.get(pk=actor_pk)
#     serializer = ActorSerializer(actor)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def director_detail(request, director_pk):
#     director = get_object_or_404(Director, pk=director_pk)
#     director = Director.objects.get(pk=director_pk)
#     serializer = DirectorSerializer(director)
#     return Response(serializer.data)


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def review_create_or_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    else:  # POST, Create an movie
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_or_update_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:  # DELETE
        review.delete()
        return Response('Delete success', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_comment_create_or_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        comments = review.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    else:  # POST
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review)
            return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_comment_detail_or_update_delete(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:  # DELETE
        review.delete()
        return Response('Delete success', status=status.HTTP_204_NO_CONTENT)
