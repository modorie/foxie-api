from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer, ProfileViewSerializer


@api_view(['POST'])
def profile_create(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def profile_detail_or_update(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.method == 'GET':
        serializer = ProfileViewSerializer(profile)
        return Response(serializer.data)

    elif request.user and request.user.is_authenticated:
        serializer = ProfileSerializer(data=request.data, instance=profile)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def follow(request, username):
    me = get_object_or_404(Profile, user__username=request.user.username)
    you = get_object_or_404(Profile, user__username=username)
    if me != you:
        if you.followers.filter(user__username=me.user.username).exists():
            you.followers.remove(me)
        else:
            you.followers.add(me)

    data = {
        'follow_count': len(you.followers.all()),
        'is_followed': you.followers.filter(user__username=me.user.username).exists()
    }

    return Response(data, status=status.HTTP_200_OK)
