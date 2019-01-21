from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify

from authors.apps.authentication.models import User

class Article(models.Model):
    """
        Each Article model schema
    """
    image_path = CloudinaryField(blank=True, null=True)
    slug = models.SlugField(max_length=255)
    title = models.CharField(db_index=True, max_length=255)
    body = models.CharField(db_index = True, max_length=8055)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favourites = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
