from datetime import datetime

from accounts.models import User
from rest_framework import serializers
from .models import Posts


class CreatePostSerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField('time_format')
    username = serializers.SerializerMethodField('display_username')

    class Meta:
        model = Posts
        fields = ['id', 'user', 'content', 'created_on', 'username'
                 ,'title']

    def display_username(self, post):
        return post.user.get_username()

    def create(self, validated_data):
        """ Creates and returns a new user """
        new_post = Posts(
            user=validated_data.get('user'),
            content=validated_data.get('content'),
            title=validated_data.get('title'),
            created_on=datetime.utcnow()
        )

        new_post.save()
        return new_post

    def update(self, post, validated_data):
        post.content = validated_data.get('content')
        post.title=validated_data.get('title')
        post.save()
        return post

    def time_format(self, post):
        new_time = post.created_on.strftime("%m/%d/%Y %I:%M:%S %p UTC")
        return new_time


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'user', 'content', 'created_on'
                 ,'title']