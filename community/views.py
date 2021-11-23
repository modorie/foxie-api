from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny

from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleViewSerializer, ArticleListSerializer, CommentSerializer, CommentListSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def article_list(request):
    articles = Article.objects.order_by('-pk')
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = ArticleViewSerializer(article)
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def article_update_or_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'PUT':
        serializer = ArticleSerializer(data=request.data, instance=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    else:
        article.delete()
        return Response('delete success', status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def article_likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)

    data = {
        'like_count': len(article.like_users.all()),
        'is_liked': article.like_users.filter(pk=request.user.pk).exists()
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def comment_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comments.all()
    serializer = CommentListSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def comment_update_or_delete(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response('delete success', status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def comment_likes(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)

    data = {
        'like_count': len(comment.like_users.all()),
        'is_liked': comment.like_users.filter(pk=request.user.pk).exists()
    }

    return Response(data)
