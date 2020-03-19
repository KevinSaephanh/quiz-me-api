from rest_framework import serializers
from .models import CustomUser
from _datetime import date


class UserSerializer(serializers.ModelSerializer):
    def update(self, validated_data, pk):
        user = CustomUser.objects.get(pk=pk)
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.password = validated_data['password']
        user.bio = validated_data['bio']
        user.profile_pic = validated_data['profile_pic']
        user.updated_at = date.today()
        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio', 'profile_pic']
