import time
from datetime import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializer import PostSerializer
from .models import Posts


# Create your views here.
class PostView(APIView):
    def get(self, request):
        user = request.user
        data = Posts.objects.filter(user=user)
        print(data)
        serializer = PostSerializer(data, many=True)
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            user = request.user
            print(user.username)

        except:
            Response(data={'error': {'message': 'You are not allowed to take this action'}},
                     status=status.HTTP_401_UNAUTHORIZED)

        data = {
            'content': request.data['content'],
            'title': request.data['title'],
            'user': user.id,
        }

        serializer = PostSerializer(data=data)
        print(data)

        # make sure the data given to the user is valid
        if serializer.is_valid():
            print(datetime.now())
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # return all the erros if it was not successfull
            return Response(data={'error': {'message': 'unable to process request'}},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            post = Posts.objects.get(pk=post_id)
            if post.user != request.user:
                return Response(data={'error': {'message': 'You are not allow to delete this post'}},
                                status=status.HTTP_401_UNAUTHORIZED)
            post.delete()
            return Response(data={'message': 'post was deleted'}, status=status.HTTP_200_OK)

        # in case the post was not found
        except Posts.DoesNotExist:
            return Response(data={'error': {'message': 'post was not found'}}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, post_id):

        try:
            post = Posts.objects.get(pk=post_id)
            user=request.user
            data = {
                'title':request.data['title'],
                'content': request.data['content'],
                'postId': post_id,
                'user': user.id,
            }
            if post.user != request.user:

                return Response(data={'error': {'message': 'You are not allow to edit this post'}},
                                status=status.HTTP_401_UNAUTHORIZED)
            post_title=''
            post_content=''
            try:
                post_title=request.data['title']
            except KeyError:
                post_title=post.title
            try:
                post_content=request.data['content']
            except KeyError:
                post_content=post.content
            post.title=post_title
            post.content=post_content
            serializer=PostSerializer(post,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_200_OK)

        # in case the post was not found
        except Posts.DoesNotExist:
            print('Hiii')
            time.sleep(10)
            return Response(data={'error': {'message': 'post was not found'}}, status=status.HTTP_404_NOT_FOUND)
