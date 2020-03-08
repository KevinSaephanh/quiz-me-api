from django.shortcuts import render
from rest_framework import permissions, status, pagination
from rest_framework.decorators import permission_classes
from .models import Profile
from .serializers import ProfileSerializer
from quiz_me.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from requests.models import Response


# Find profile using username
def get_profile_object(username):
    try:
        user = User.objects.get(username=username)
        return Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        raise Exception('Profile does not exist')


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def profile_list(request, page):
    try:
        queryset = Profile.objects.all()
    except Profile.DoesNotExist:
        return Response({'error': 'No profiles found'}, status=status.HTTP_404_NOT_FOUND)

    # Set up pagination for profiles
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 10
    paginator.page = page

    # Create paginated profile list
    paginated_profiles = paginator.paginate_queryset(queryset, request)
    serializer = ProfileSerializer(paginated_profiles, many=True)
    if serializer is not None:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_profile(request, username):
    serializer = ProfileSerializer.create(request, username)
    if serializer is not None:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_profile_by_username(request, username):
    profile = get_profile_object(username)
    if profile is not None:
        return Response(profile, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAdminUser, IsOwnerOrReadOnly])
def update_delete_profile(request, username):
    if request.method == 'PUT':
        serializer = ProfileSerializer.update(request, username)
        if serializer is not None:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        profile = get_profile_object(username)
        if profile is not None:
            profile.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)
