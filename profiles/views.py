from django.shortcuts import render
from rest_framework import permissions, response, status, viewsets, generics, views
from .models import Profile
from .serializers import ProfileSerializer
from quiz_me.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from requests.models import Response


class ProfileListView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, format=None):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)


class ProfileCreateView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, username):
        quiz = ProfileSerializer.create(self, request, username)

        if quiz is not None:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveUpdateDestroyView(views.APIView):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Exception('Profile does not exist')

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)

        if serializer.is_valid():
            user = User.objects.all(pk=serializer.data.user)
            response_data = {}
            response_data['bio'] = serializer.data.bio
            response_data['profile_pic'] = serializer.data.profile_pic
            response_data['username'] = user.username
            response_data['email'] = user.email

            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile successfully updaetd'}, status=status.HTTP_200_OK)
        return Response({'error': 'Unable to update profile'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)

        if profile is not None:
            profile.delete()
            return Response({'message': 'Profile successfully deleted'}, status=status.HTTP_200_OK)
        return Response({'error': 'Unable to delete profile'}, status=status.HTTP_404_NOT_FOUND)
