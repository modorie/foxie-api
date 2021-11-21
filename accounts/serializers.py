from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from rest_framework import serializers

from .models import Profile
from movies.models import Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = list(obj.user.movies_review.all().values('id', 'movie', 'rank'))
        return reviews

    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'avatar', 'tags', 'content', 'followers', 'reviews')
