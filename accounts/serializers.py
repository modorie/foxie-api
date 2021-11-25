from django.contrib.auth import get_user_model
from django.db.models import Subquery, Count, F

from rest_framework import serializers

from .models import Profile
from movies.models import Movie

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'avatar', 'tags', 'content')


class ProfileViewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()
    movies = serializers.SerializerMethodField()
    favorite_genres = serializers.SerializerMethodField()
    favorite_actors = serializers.SerializerMethodField()
    favorite_directors = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = list(obj.user.movies_review.all().values().annotate(movie=F('movie_id')))
        return reviews

    def get_movies(self, obj):
        movies = Movie.objects.filter(id__in=Subquery(obj.user.movies_review.all().values('movie')))
        return movies.values('id', 'title', 'vote_average', 'poster_path')

    def get_favorite_genres(self, obj):
        genre_counts = obj.user.movies_review.all().values('movie__genre_ids').annotate(genre=F('movie__genre_ids__name')).annotate(count=Count('movie__genre_ids'))
        return genre_counts

    def get_favorite_actors(self, obj):
        actors_counts = obj.user.movies_review.all().values('movie__actors').annotate(genre=F('movie__actors__name')).annotate(count=Count('movie__actors'))
        return actors_counts

    def get_favorite_directors(self, obj):
        actors_counts = obj.user.movies_review.all().values('movie__directors').annotate(genre=F('movie__directors__name')).annotate(count=Count('movie__directors'))
        return actors_counts

    class Meta:
        model = Profile
        fields = (
            'user', 'nickname', 'avatar', 'tags', 'content', 'followers', 'followings',
            'reviews', 'movies', 'favorite_genres', 'favorite_actors', 'favorite_directors')
