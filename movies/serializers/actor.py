from rest_framework import serializers
from ..models import Actor, Casting


class CastingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Casting
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):

    castings = CastingSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = '__all__'
