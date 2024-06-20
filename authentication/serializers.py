from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "first_name", "phone", "email"]


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
