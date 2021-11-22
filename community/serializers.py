from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Article, Comment
from accounts.models import Profile

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):

        class ProfileSerializer(serializers.ModelSerializer):

            class Meta:
                model = Profile
                fields = ('user', 'nickname', 'avatar')

        profile = ProfileSerializer(read_only=True)

        class Meta:
            model = User
            fields = ('id', 'username', 'profile')

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'created_at', 'updated_at',)


class ArticleSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):

        class ProfileSerializer(serializers.ModelSerializer):

            class Meta:
                model = Profile
                fields = ('user', 'nickname', 'avatar')

        profile = ProfileSerializer(read_only=True)

        class Meta:
            model = User
            fields = ('id', 'username', 'profile')

    author = UserSerializer(read_only=True)

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author', 'comments')


class ArticleListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )
    likes_count = serializers.IntegerField(
        source='like_users.count'
    )

    class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('id', 'username')

    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'author', 'comments_count', 'created_at', 'likes_count')
