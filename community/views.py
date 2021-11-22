from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleListSerializer, CommentSerializer


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


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_or_update_or_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(data=request.data, instance=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    else:
        article.delete()
        return Response('delete success', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def comment_create_or_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    else:
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data)


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
