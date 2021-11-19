from rest_framework import serializers
from ..models import Genre, Movie, Actor, Casting


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)


class MovieSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    genre_ids = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
