from rest_framework import serializers

from .models import User
from datetime import datetime

from upload.models import Posts
from upload.serializer import PostSerializer


class AccountRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user.created_on=datetime.now()
        user.update_on=datetime.now()
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.bio = validated_data.get('bio')
        instance.full_name = validated_data('full_name')
        instance.update_on = datetime.now()
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField('get_user_posts')

    class Meta:
        model = User
        fields = ['id','username', 'email', 'date_joined','posts']

    def get_user_posts(self,user):
        post = Posts.objects.filter(user=user.id)
        serializer = PostSerializer(post, many=True)
        return serializer.data
