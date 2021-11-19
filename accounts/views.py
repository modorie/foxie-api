from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer


@api_view(['GET', 'PUT'])
def profile_detail_or_update(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(data=request.data, instance=profile)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def follow(request, username):
    me = get_object_or_404(Profile, username=request.user.username)
    you = get_object_or_404(Profile, username=username)
    if me != you:
        if you.followers.filter(username=me.user.username).exists():
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return Response('Success', status=status.HTTP_200_OK)
