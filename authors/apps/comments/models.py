from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile


class Comments(models.Model):

    author_profile = models.ForeignKey(Profile, related_name='author_profile', on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author_profile)
