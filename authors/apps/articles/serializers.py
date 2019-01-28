from django.core.exceptions import ValidationError

from authors.apps.like_dislike.serializers import PreferenceSerializer
from authors.apps.authentication.messages import statusmessage
from authors.apps.like_dislike.models import LikeDislike
from rest_framework import serializers
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from ..authentication.serializers import RegistrationSerializer
from .messages import error_msgs
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
        Article model serializers
    """
    author = RegistrationSerializer(many=False, read_only=True, required=False)
    image_path = serializers.ImageField(default=None)
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    dislike_count = serializers.SerializerMethodField(read_only=True)
    like_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"

    def create_slug(self, title):
        """
            Create a slag
        """
        a_slug = slugify(title)
        origin = 1
        unique_slug = a_slug
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(a_slug, origin)
            origin += 1
        slug = unique_slug
        return slug

    def get_like_count(self, obj):
        """ Return the number of likes"""

        return obj.prefs.count('likes')

    def get_dislike_count(self, obj):
        """Return the nimber of dislikes"""

        return obj.prefs.count('dislikes')

    def get_like_status(self, obj):
        """Get my preference"""
        user = self.context['request'].user
        content_type = ContentType.objects.get_for_model(
            obj)
        try:
            item = LikeDislike.objects.get(
                content_type=content_type, object_id=obj.id, user=user)
            return statusmessage['Like'] if item.pref == 1 else statusmessage['Dislike']

        except Exception as e:
            if e.__class__.__name__ == "DoesNotExist":
                return statusmessage['Null']
