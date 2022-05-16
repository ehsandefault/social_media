from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
from django.db.models import CASCADE


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=40)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=200, blank=True)
    profile_image = models.CharField(max_length=1000,
                                    default="https://res.cloudinary.com/dgknrkenk/image/upload/v1579667401/uwjxuqzu4baspaqybrmp.png")

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    full_name = models.CharField(blank=False)

    def __str__(self):
        return self.full_name

    class Meta:
        app_label = 'accounts'
