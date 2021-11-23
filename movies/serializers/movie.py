from rest_framework import serializers
from ..models import Genre, Movie, Actor, Casting, Director


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'release_date', 'vote_average')


class MovieSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    class DirectorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Director
            fields = '__all__'

    class CastingSerializer(serializers.ModelSerializer):

        class ActorSerializer(serializers.ModelSerializer):
            class Meta:
                model = Actor
                fields = '__all__'

        actor = ActorSerializer(read_only=True)

        class Meta:
            model = Casting
            fields = '__all__'

    castings = CastingSerializer(many=True, read_only=True)
    genre_ids = GenreSerializer(many=True, read_only=True)
    directors = DirectorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'adult', 'release_date', 'popularity', 'vote_count', 'vote_average',
                  'overview', 'original_language', 'original_title', 'genre_ids', 'directors',
                  'backdrop_path', 'poster_path', 'videos', 'recommendations', 'castings')
