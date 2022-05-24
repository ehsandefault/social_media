import time
from datetime import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializer import CreatePostSerializer, PostSerializer
from .models import Posts


# Create your views here.

class UploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {
            'content': request.data['content'],
            'title': request.data['title'],
            'user': request.user.id,
        }

        serializer = CreatePostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        if Posts.objects.filter(pk=post_id).exists():
            data = Posts.objects.get(pk=post_id)
            serializer = PostSerializer(data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': {'message': 'post was not found'}}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        if Posts.objects.filter(pk=post_id).exists():
            post = Posts.objects.get(pk=post_id)
            if post.user != request.user:
                return Response(data={'error': {'message': 'You are not allow to delete this post'}},
                                status=status.HTTP_401_UNAUTHORIZED)
            post.delete()
            return Response(data={'message': 'post was deleted'}, status=status.HTTP_200_OK)

        else:
            return Response(data={'error': {'message': 'post was not found'}}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, post_id):

        if Posts.objects.filter(pk=post_id).exists():
            post = Posts.objects.get(pk=post_id)
            user = request.user
            data = {
                'title': request.data['title'],
                'content': request.data['content'],
                'postId': post_id,
                'user': user.id,
            }
            if post.user != request.user:
                return Response(data={'error': {'message': 'You are not allow to edit this post'}},
                                status=status.HTTP_401_UNAUTHORIZED)

            post_title = request.data.get('title', None)
            if post_title:
                post.title = post_title
            post_content = request.data.get('content', None)
            if post_content:
                post.content = post_content

            serializer = CreatePostSerializer(post, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': {'message': 'post was not found'}}, status=status.HTTP_404_NOT_FOUND)
