from rest_framework import serializers
from ..models import Movie, Actor, Casting


class CastingSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('id', 'title',)

    class ActorSerializer(serializers.ModelSerializer):

        class Meta:
            model = Actor
            fields = '__all__'

    movie_id = MovieSerializer(many=True, read_only=True)
    actor_id = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Casting
        fields = '__all__'
