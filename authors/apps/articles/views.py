import os
import django
import json
import random
import datetime as dt

from rest_framework import status, exceptions
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime, timedelta
from rest_framework.views import Response
from django.shortcuts import get_object_or_404

from .renderers import ArticleJSONRenderer
from .models import Article
from .serializers import ArticleSerializer
from .messages import error_msgs, success_msg


class ArticleAPIView(generics.ListCreateAPIView):
    """
        Article endpoints
    """
    renderer_classes = (ArticleJSONRenderer,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request):
        """
            POST /api/v1/articles/
        """
        permission_classes = (IsAuthenticated,)
        context = {"request": request}
        article = request.data.copy()

        article['slug'] = ArticleSerializer(
        ).create_slug(request.data['title'])
        serializer = self.serializer_class(data=article, context=context)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        """
            GET /api/v1/articles/
        """
        permission_classes = (AllowAny,)
        queryset = self.get_queryset()
        serializer = ArticleSerializer(
            queryset,
            context={
                'request': request
            },
            many=True
        )
        return Response(serializer.data, status=200)


class SpecificArticle(generics.RetrieveUpdateDestroyAPIView):
    """
        Specific article endpoint class
    """
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)

    def get(self, request, slug, *args, **kwargs):
        """
            GET /api/v1/articles/<slug>/
        """
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise exceptions.NotFound({
                "message": error_msgs['not_found']
            })
        serializer = ArticleSerializer(
            article,
            context={
                'request': request
            }
        )
        return Response(serializer.data, status=200)

    def delete(self, request, slug, *args, **kwargs):
        """
            DELETE /api/v1/articles/<slug>/
        """
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise exceptions.NotFound({
                "message": error_msgs['not_found']
            })
        if request.user.id != article.author_id:
            return Response({
                "message": error_msgs["article_owner_error"]
            }, status=403)
        else:
            article.delete()
            return Response({
                "article": success_msg['article_delete']
            }, status=204)

    def put(self, request, slug, *args, **kwargs):
        """
            PUT /api/v1/articles/<slug>/
        """
        article = get_object_or_404(Article.objects.all(), slug=slug)
        if request.user.id != article.author_id:
            return Response({
                "message": error_msgs['article_owner_error']
            }, status=403)
        else:
            article_data = request.data
            article.updated_at = dt.datetime.utcnow()
            article.title = article_data['title']
            article.image_path = article_data['image_path']
            article.body = article_data['body']
            serializer = ArticleSerializer(
                instance=article, data=article_data,
                context={'request': request}, partial=True
            )
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(
                    [
                        serializer.data,
                        [{"message": success_msg['article_update']}]
                    ], status=201
                )
            else:
                return Response(
                    serializer.errors,
                    status=400
                )
