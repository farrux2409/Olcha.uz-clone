# from django.shortcuts import render
#
# # Create your views here.
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.core.exceptions import ObjectDoesNotExist
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import RegisterSerializer, UserSerializer, UserModelSerializer
from rest_framework.authtoken.models import Token

from .serializers import *


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class RegisterUserAPI(generics.GenericAPIView):
    serializer_class = UserModelSerializer

    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)
        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj)})


# Homework starts here --->>


# class LoginUserAPI(KnoxLoginView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Doesnot exist!"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user = User.objects.get(username=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=User.objects.get(username=serializer.validated_data['username'])).key
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)


class UserJWTLogin(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginJwtSerializer(data=data)
            if serializer.is_valid():
                password = serializer.data['password']
                username = serializer.data['username']
                user = authenticate(username=username, password=password)
                if user is not None:
                    return Response(
                        {
                            "status": 400,
                            "message": "Invalid Password",
                            "data": {}
                        }
                    )
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }


        except Exception as e:
            print(e)


class JWTRegisterAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserTokenSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "Register Successful",
                    "data": serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
