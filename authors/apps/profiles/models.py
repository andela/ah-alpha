from django.db import models
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField

# local import
from ..authentication.models import User


class Profile(models.Model):
    """

    Here create the profiles models, we decaler the fields we want included

    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profiles')
    bio = models.TextField(blank=True)
    image = CloudinaryField(
        "image",
        default='https://res.cloudinary.com/dxecwuaqd/image/upload/v1548231850/jrp16w4auxhj0da6jcbk.png')
    First_name = models.CharField(max_length=50, blank=True)
    Last_name = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    # returns string representation of object

    def __str__(self):
        return str(self.user.username)


def create_profile(sender, instance, created, **kwargs):
    # this creates a user profile when a user object is created
    if created:
        instance.profile = Profile.objects.create(user=instance)


# this saves the user profile created
post_save.connect(create_profile, sender=User)
