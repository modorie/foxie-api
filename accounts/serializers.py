from django.contrib.auth import get_user_model
from django.db.models import Subquery

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

    def get_reviews(self, obj):
        reviews = list(obj.user.movies_review.all().values())
        return reviews

    def get_movies(self, obj):
        movies = Movie.objects.filter(id__in=Subquery(obj.user.movies_review.all().values('movie')))
        return movies.values('id', 'title', 'vote_average', 'poster_path')

    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'avatar', 'tags', 'content', 'followers', 'followings', 'reviews', 'movies')
