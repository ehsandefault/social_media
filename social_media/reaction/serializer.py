from rest_framework import serializers

from .models import User
from datetime import datetime

from upload.models import Posts
from .models import Like, Follower
from upload.serializer import PostSerializer
# from accounts.serializer.py import ProfileSerializer

class LikeSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField('get_posts')

    class Meta:
        model = Like
        fields = ['posts']

    def get_posts(self, liked_posts):
        post = Posts.objects.filter(liked_posts.post_id)
        serializers = PostSerializer(post, many=True)
        return serializers.data


class FollowSerializer(serializers.ModelSerializer):
    # user=ProfileSerializer(many=true,)
    class Meta:
        model = Follower
        fields = ['following','user']

        def create(self, validated_data):
            follower = Follower(
                followed=validated_data.get('following'),
                followed_by=validated_data.get('followed_by')
            )

            follower.created_on = datetime.now()
            follower.save()
            return follower
