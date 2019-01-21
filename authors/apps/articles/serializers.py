from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.template.defaultfilters import slugify

from  .models import Article
from ..authentication.serializers import RegistrationSerializer
from .messages import error_msgs

class ArticleSerializer(serializers.ModelSerializer):
    """
        Article model serializers
    """
    author = RegistrationSerializer(many=False, read_only=True, required=False)
    image_path = serializers.ImageField(default=None)
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
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
