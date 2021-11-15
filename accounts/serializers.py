from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    nickname = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    passwordConfirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 'passwordConfirmation')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['passwordConfirmation']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            nickname=validated_data['nickname'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user