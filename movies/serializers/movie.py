from rest_framework import serializers
from ..models import Actor, Director, Genre, Movie, Review


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)


class MovieSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    class ActorSerializer(serializers.ModelSerializer):

        class Meta:
            model = Actor
            fields = '__all__'

    class DirectorSerializer(serializers.ModelSerializer):

        class Meta:
            model = Director
            fields = '__all__'

    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    directors = DirectorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
