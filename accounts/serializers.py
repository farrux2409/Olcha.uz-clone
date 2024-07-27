from rest_framework import serializers
# from app.models import User

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'<write only true>': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'])
        # user = User.objects.create_superuser(validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(write_only=True)

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise serializers.ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise serializers.ValidationError({"message": "Both password must match"})
        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'username']
        extra_kwargs = {'password': {'write_only': True}}


class VerifyAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField()


class LoginJwtSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
