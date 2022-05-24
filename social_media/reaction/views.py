import time

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
# Create your views here.
from .models import Like, Follower
from .serializer import LikeSerializer, FollowSerializer
from upload.models import Posts
from accounts.models import User
from datetime import datetime


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        def get(self, request, post_id):
            user = request.user
            user = User.objects.get(username=user.user_name)
            already_liked = Like.objects.filter(post_id=post_id, liked_by=user)
            if len(already_liked) == 0:
                liked =Like(post_id=post_id, liked_by=user)
                liked.created_on = datetime.now()
                liked.save()
                data = {
                    'Liked by':user.username,
                    'post': post_id}
                return Response(data, HTTP_202_ACCEPTED)

            data = {
                'Error': 'Post Already Liked'}
            return Response(data)



class FollowView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_name):
        user = request.user
        followed = User.objects.get(username=user_name)
        followed_by = User.objects.get(username=user.username)
        already_followed = Follower.objects.filter(followed=followed, followed_by=followed_by)
        if len(already_followed) == 0:
            follow = Follower(followed=followed, followed_by=followed_by)
            follow.created_on = datetime.now()
            follow.save()
            data = {
                'followed': followed.username,
                'followed_by': followed_by.username}
            return Response(data, HTTP_202_ACCEPTED)

        data = {
            'Error': 'User Already Followed'}
        return Response(data)
