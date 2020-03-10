from rest_framework import serializers
from .models import CustomUser
from _datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio', 'profile_pic']
