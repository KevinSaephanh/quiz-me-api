from .models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    def create(self, request, username):
        data = request.data
        profile = Profile()
        profile.user = User.objects.get(username=username)
        profile.bio = data['bio']
        profile.profile_pic = data['profile_pic']
        profile.save()
        return profile

    def update(self, request, username):
        data = request.data
        profile = Profile()

        # Update user info associated with profile
        user = User.objects.get(username=username)
        user.username = data['username']
        user.email = data['email']
        user.password = data['password']

        # Update profile
        profile.user = user
        profile.bio = data['bio']
        profile.profile_pic = data['profile_pic']
        profile.save()
        return profile

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']
