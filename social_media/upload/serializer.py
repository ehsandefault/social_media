from datetime import datetime

from rest_framework import serializers
from .models import Posts


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'user', 'content', 'created_on', 'title']

    def create(self, validated_data):
        new_post = Posts(
            user=validated_data.get('user'),
            content=validated_data.get('content'),
            title=validated_data.get('title'),
        )

        new_post.save()
        return new_post

    def update(self, post, validated_data):
        post.content = validated_data.get('content')
        post.title = validated_data.get('title')
        post.save()
        return post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['content', 'title']
