from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
from django.db.models import CASCADE


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         print('Here created')
#         Token.objects.create(user=instance)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=40)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=200, default=" ", blank=True)
    profileImage = models.CharField(max_length=1000,
                                    default="https://res.cloudinary.com/dgknrkenk/image/upload/v1579667401/uwjxuqzu4baspaqybrmp.png")
    follower = models.IntegerField(default=0)
    created_on = models.TimeField()
    update_on = models.TimeField()
    full_name = models.TextField(blank=False)

    def __str__(self):
        return self.full_name

