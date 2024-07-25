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
from accounts.serializers import RegisterSerializer, UserSerializer, UserModelSerializer
from rest_framework.authtoken.models import Token


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

# class LoginUserAPI(KnoxLoginView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
