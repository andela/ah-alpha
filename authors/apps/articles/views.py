import datetime as dt
import json
import os
import random
from datetime import datetime, timedelta

import django
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from authors.apps.authentication.utils import status_codes, swagger_body
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method
from rest_framework import exceptions, generics, status
from rest_framework import status, exceptions
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from datetime import datetime, timedelta
from rest_framework.views import Response

from .renderers import ArticleJSONRenderer
from .models import Article, Tags
from .serializers import ArticleSerializer, TagSerializers
from .messages import error_msgs, success_msg
from authors.apps.core.pagination import PaginateContent

from authors.apps.reading_stats.models import ReadStats


class ArticleAPIView(generics.ListCreateAPIView):
    """
        Article endpoints
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @swagger_auto_schema(
        request_body=swagger_body(prefix="article", fields=(
            'image_path', 'title', 'body')),
        responses=status_codes(codes=(201, 400))
    )
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
        perform_pagination = PaginateContent()
        objs_per_page = perform_pagination.paginate_queryset(self.queryset, request)
        serializer = ArticleSerializer(
            objs_per_page,
            context={
                'request': request
            },
            many=True
        )
        return perform_pagination.get_paginated_response(serializer.data)


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
        #this checks if an istance of read exists 
        #if it doesn't then it creates a new one
        if request.user.id:
            if not ReadStats.objects.filter(user=request.user, article=article).exists():
                user_stat = ReadStats(
                    user = request.user,
                    article = article
                )
                user_stat.article_read = True
                user_stat.save()

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
            serializer = ArticleSerializer(
                instance=article,
                data=article_data,
                context={'request': request},
                partial=True
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


class TagAPIView(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, *args):
        """
            GET /api/v1/tags/
        """
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)

        if data:
            return Response({
                'message': success_msg['tag_get'],
                'tags': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': error_msgs['tags_not_found'],
        }, status=status.HTTP_404_NOT_FOUND)

