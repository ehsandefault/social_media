from django.db import models
from accounts.models import User


# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.CharField(max_length=1000)
    created_on = models.DateTimeField()
    title=models.TextField()

