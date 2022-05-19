from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializer import AccountRegistrationSerializer, AccountSerializer
from .models import User


# Create your views here.
class UserDetailsView(APIView):

    def get(self, request, username):
        if User.filter(username=username).exists():
            user = User.objects.get(username=username)
            account_serializer = AccountSerializer(instance=user)
            return Response(account_serializer.data)
        else:
            return Response(data={'error': {'message': 'user not found'}}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get("password", None)
        if email is None or password is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check if a user with such username or email exist
        user = None
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
        else:
            return Response({'error': 'Such user was not found'},
                            status=status.HTTP_404_NOT_FOUND)
        username = user.username
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        print(token.key)
        data = {
            "success": True,
            "token": token.key,
            "username": user.username,
            "email": user.email,

        }
        return Response(data=data, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request):
        serializer = AccountRegistrationSerializer(request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            Token.objects.create(user=new_user)
            data = {
                'success': 'User created',
                'User id': new_user.id,
                'User name': new_user.username,
                'User email': new_user.email,
                'token': Token.objects.get(user=new_user).key,
            }

            return Response(data, status=status.HTTP_201_CREATED)
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        data = request.data
        new_password = data.get('new_password', None)
        old_password = data.get('password', None)
        email = data.get('email', None)
        if new_password is None or old_password is None or email is None:
            return Response(data={'message': 'This was an invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        current_user = None
        if User.objects.filter(email=email).exists():
            current_user = User.objects.get(email=email)
        else:
            return Response(data={'message': 'This user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        username = current_user.username
        user = authenticate(username=username, password=old_password)
        if not user:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        current_user.set_password(new_password)
        current_user.save()

        token, _ = Token.objects.get_or_create(user=current_user)

        data = {
            'email': current_user.email,
            'username': current_user.username,
            'password': new_password,
            'token': token.key
        }

        return Response(data=data, status=status.HTTP_200_OK)
