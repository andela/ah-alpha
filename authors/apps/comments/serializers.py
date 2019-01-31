from rest_framework import serializers
from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import UserProfileSerializer
from .models import Comments


class CommentSerializer(serializers.ModelSerializer):
    """
       Serializer class for comments
    """
    author_profile = UserProfileSerializer(
        many=False, read_only=True, required=False)

    class Meta:
        model = Comments
        fields = ('article', 'id', 'created_at', 'updated_at',
                  'body', 'author_profile')

        read_only_fields = ('id', 'author_profile',
                            'created_at', 'updated_at', 'article')
                                          