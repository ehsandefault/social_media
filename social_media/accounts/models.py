from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .constant import PROFILE_AVTAR
# Create your models here.
from django.db.models import CASCADE


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=40)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=200, blank=True)
    profileImage = models.CharField(max_length=1000,
                                    default=PROFILE_AVTAR)
    follower = models.IntegerField(default=0)
    created_on = models.TimeField()
    updated_on = models.TimeField()

    def __str__(self):
        return self.username

