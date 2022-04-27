from django.db import models
from accounts.models import User
from upload.models import Posts


# Create your models here.
class Like(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField()


class Comment(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField()


class Follower(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE,related_name='followed_user')
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='followed_by')
    created_on = models.DateTimeField()


class Reply(models.Model):
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='replied_by')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField()
    created_on = models.DateTimeField()
