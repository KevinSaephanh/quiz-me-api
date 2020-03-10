from django.shortcuts import render

from rest_framework import permissions, status, viewsets, pagination, mixins
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Category, Quiz, Vote
from .serializers import QuizSerializer, VoteSerializer, CategorySerializer
from rest_framework.response import Response
from quiz_me.permissions import IsOwnerOrReadOnly


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


class QuizViewSet(viewsets.ViewSet):
    serializer_class = QuizSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication]

    # Used for retrieve, update, and destroy methods
    def get_queryset(self, pk):
        try:
            queryset = Quiz.objects.filter(pk=pk)
            return queryset
        except Quiz.DoesNotExist:
            raise Exception('Quiz does not exist')

    def create(self, request):
        serializer = self.serializer_class.create(request)
        if serializer is not None:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        quiz = self.get_queryset(pk)
        if quiz is not None:
            return Response(quiz, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        quiz = self.get_queryset(pk)
        if quiz is not None:
            serializer = QuizSerializer(quiz, data=request.data)
            serializer.save()
            return Response(serializer, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        quiz = self.get_queryset(pk)
        if quiz is not None:
            quiz.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

# Get quizzes in paginated form
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def quiz_list(request, page):
    # Set up pagination for quizzes
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 10
    paginator.page = page

    # Create paginated quiz list
    queryset = Quiz.objects.all().order_by('-created_at')
    paginated_quizzes = paginator.paginate_queryset(queryset, request)
    serializer = QuizSerializer(paginated_quizzes, many=True)
    if serializer is not None:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


# Get all quizzes by category name
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
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
