from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify
from authors.apps.authentication.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from authors.apps.like_dislike.models import LikeDislike


class Article(models.Model):
    """
        Each Article model schema
    """
    image_path = CloudinaryField(blank=True, null=True)
    slug = models.SlugField(max_length=255)
    title = models.CharField(db_index=True, max_length=255)
    body = models.TextField(db_index=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favourites = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, related_name="author", on_delete=models.CASCADE)
    prefs = GenericRelation(LikeDislike, related_query_name='articles')

    objects = models.Manager()

    def __str__(self):
        return self.title
