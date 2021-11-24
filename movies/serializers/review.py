from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Movie, Review, Comment
from accounts.models import Profile

User = get_user_model()


class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewViewSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):

        class ProfileSerializer(serializers.ModelSerializer):

            class Meta:
                model = Profile
                fields = ('user', 'nickname', 'avatar',)

        profile = ProfileSerializer(read_only=True)

        class Meta:
            model = User
            fields = ('id', 'username', 'profile')

    comments = CommentSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ()
