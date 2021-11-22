from rest_framework import serializers
from ..models import Movie, Review, Comment


class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'title', 'author',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('id', 'title', 'vote_average', 'overview', 'genre_ids', 'poster_path')

    movie = MovieSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'username', 'movie_id', 'comment_id', 'like_users')
