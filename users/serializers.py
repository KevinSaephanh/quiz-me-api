from rest_framework import serializers
from .models import CustomUser
from _datetime import date
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings


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


# JWT related variables
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class CustomJWTSerializer(JSONWebTokenSerializer):
    username_field = 'username'

    def validate(self, request):
        username = request.get('username')
        password = request.get('password')
        user_obj = CustomUser.objects.filter(username=username)

        if user_obj is not None:
            credentials = {
                'username': username,
                'password': password
            }

            if all(credentials.values()):
                try:
                    user = authenticate(**credentials)

                    user_details = {
                        'id': user.pk,
                        'username': user.username,
                        'profilePic': user.profile_pic
                    }
                    payload = jwt_payload_handler(user)
                    return {'token': jwt_encode_handler(payload), 'user': user}
                except:
                    raise serializers.ValidationError(
                        'Unable to login with provided credentials')
        else:
            raise serializers.ValidationError(
                'Username and/or password does not match any user in the database')
