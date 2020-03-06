from django.shortcuts import render

from rest_framework import permissions, status, viewsets, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.throttling import UserRateThrottle

from .models import Category, Quiz, Vote
from .serializers import QuizSerializer, VoteSerializer, CategorySerializer
from rest_framework.response import Response
from quiz_me.permissions import IsOwnerOrReadOnly


class TenPerDayUserThrottle(UserRateThrottle):
    rate = '10/day'


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = pagination.PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.PageNumberPagination


# Find quiz by pk
def get_quiz_object(pk):
    try:
        return Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        raise Exception('Quiz does not exist')


# Create a quiz
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
@throttle_classes([OncePerDayUserThrottle])
def create_quiz(request):
    if request.method == 'POST':
        serializer = QuizSerializer.create(request)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# Get all quizzes
@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def quiz_list(request, page):
    try:
        queryset = Quiz.objects.all().order_by('-created_at')
    except Quiz.DoesNotExist:
        return Response({'error': 'No quizzes found'}, status=status.HTTP_404_NOT_FOUND)

    # Set up pagination for quizzes
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 10
    paginator.page = page

    # Create paginated quiz list
    paginated_quizzes = paginator.paginate_queryset(queryset, request)
    serializer = QuizSerializer(paginated_quizzes, many=True)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


# Get quiz by primary key
@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def get_quiz(request, pk):
    if request.method == 'GET':
        quiz = get_quiz_object(pk)
        if quiz is not None:
            return Response(quiz, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# Update or delete quiz by primary key
@api_view(['PUT', 'DELETE'])
@permission_classes((IsOwnerOrReadyOnly, permissions.IsAdminUser))
@throttle_classes([OncePerDayUserThrottle])
def update_delete_quiz(request, pk):
    quiz = get_quiz_object(pk)
    if quiz is not None:
        if request.method == 'PUT':
            serializer = QuizSerializer(quiz, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(quiz, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            quiz.delete()
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


# Get all quizzes by category name
@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def get_quizzes_by_category(request, category_name, page):
    try:
        retrieved_category = Category.objects.get(title=category_name)
        quiz_list = Quiz.objects.get(category=retrieved_category.pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category could not be found'}, status=status.HTTP_404_NOT_FOUND)
    except Quiz.DoesNotExist:
        return Response({'error': 'No quizzes found for category'}, status=status.HTTP_404_NOT_FOUND)

    # Set up pagination for quizzes
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 10
    paginator.page = page

    # Create paginated quiz list
    paginated_quizzes = paginator.paginate_queryset(quiz_list, request)
    serializer = QuizSerializer(paginated_quizzes, many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)
