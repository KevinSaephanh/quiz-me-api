from django.shortcuts import render

from rest_framework import permissions, generics, status, viewsets, pagination
from rest_framework.decorators import api_view, permission_classes

from .models import Category, Quiz, Vote
from .serializers import QuizSerializer, VoteSerializer, CategorySerializer
from rest_framework.response import Response


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all().order_by('-created_at')
    serializer_class = QuizSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = pagination.PageNumberPagination

    def create(self, request):
        serializer = QuizSerializer.create(request)
        if serializer.is_valid():
            quiz = serializer.create(request)
            if quiz:
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        valid_question_set = QuizSerializer.check_question_set_size(request)
        if valid_question_set is True:
            super().update(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request):
        valid_question_set = QuizSerializer.check_question_set_size(request)
        if valid_question_set is True:
            super().partial_update(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


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


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def post(request):
    if request.method == 'POST':
        serializer = QuizSerializer.create(request)
        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def list(request, page):
    try:
        queryset = Quiz.objects.all().order_by('-created_at')
    except Quiz.DoesNotExist:
        return Response({'error': 'No quizzes found for category'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Set up pagination for quizzes
        paginator = pagination.PageNumberPagination()
        paginator.page_size = 10
        paginator.page = page

        # Create paginated quiz list
        paginated_quizzes = paginator.paginate_queryset(queryset, request)
        serializer = QuizSerializer(paginated_quizzes, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)


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

    if request.method == 'GET':
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
    return Response(status=status.HTTP_400_BAD_REQUEST)
