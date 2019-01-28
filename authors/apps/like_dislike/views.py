import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views import View

from authors.apps.articles.models import Article
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method
from rest_framework import exceptions, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .messages import statusmessage, success
from .models import LikeDislike
from .renderers import LikeDislikeJSONRenderer
from .serializers import PreferenceSerializer


class PreferenceView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (LikeDislikeJSONRenderer,)
    serializer_class = PreferenceSerializer
    pref = None  # Preference type Like/Dislike
    swagger_schema = SwaggerAutoSchema

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)
        pref_status = None
        if self.pref == 'Like':
            pref_status = 1
        elif self.pref == 'Dislike':
            pref_status = -1
        try:
            obj = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(
                article), object_id=article.id, user=request.user)
            if int(obj.pref) != pref_status:
                obj.pref = pref_status
                obj.save(update_fields=['pref'])
                result, like_status = success.get(
                    self.pref), statusmessage.get(self.pref)
            else:
                obj.delete()
                result, like_status = success.get(
                    'Null'), statusmessage.get('Null')
        except Exception as e:
            if e.__class__.__name__ == "DoesNotExist":
                article.prefs.create(
                    user=request.user, pref=pref_status)
                result, like_status = success.get(
                    self.pref), statusmessage.get(self.pref)
            else:
                # Return type of error that occurred
                return Response(f" Error {e.__class__.__name__} occured")
        return Response({
            "result": result,
            "status": like_status,
            "like_count": article.prefs.count('likes'),
            "dislike_count": article.prefs.count('dislikes')
        }, status=status.HTTP_201_CREATED
        )
