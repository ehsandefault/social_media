from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializer import AccountRegistrationSerializer,AccountSerializer
from .models import User


# Create your views here.
class UserDetailsView(APIView):

    def get(self,request,username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            newdict = {'not_found': True}
            return Response(data={'error': {'message': 'user not found'}}, status=status.HTTP_404_NOT_FOUND)

        account_serializer = AccountSerializer(user)
        return Response(account_serializer.data)





class Login(APIView):
    def post(self, request):
        data = request.data
        try:
            username = data["email"]
            password = data["password"]
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check if a user with such username or email exist
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:

            try:
                user = User.objects.get(email=username)
                username = user.username
            except  User.DoesNotExist:
                return Response({'error': 'Such user was not found'},
                                status=status.HTTP_404_NOT_FOUND)

        # check to see if username with that password exist
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

        # return info of the user
        token, created = Token.objects.get_or_create(user=user)
        print(token.key)
        data = {
            "success": True,
            "token": token.key,
            "username": user.username,
            "date_joined": user.created_on,
            "email": user.email,

        }
        return Response(data=data, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = AccountRegistrationSerializer(data=data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
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


class ResetPassword(APIView):
    def post(self, request):
        try:
            new_password = request.data['new_password']
            old_password = request.data['password']
            email = request.data['email']
        except KeyError:
            return Response(data={'message': 'This was an invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(data={'message': 'This user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        username=current_user.username
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
