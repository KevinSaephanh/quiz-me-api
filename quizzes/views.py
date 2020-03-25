from django.shortcuts import render

from rest_framework import permissions, status, views, generics, viewsets, mixins, pagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.throttling import UserRateThrottle
from .models import Category, Quiz, Vote
from .serializers import QuizDetailSerializer, CreateQuizSerializer, QuizGetByTitleSerializer, QuestionSerializer, VoteSerializer, CategorySerializer
from rest_framework.response import Response
from quiz_me.permissions import IsOwnerOrReadOnly


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]
    pagination_class = pagination.PageNumberPagination

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer is not None:
            serializer.create(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = pagination.PageNumberPagination


# Get all quizzes by category name
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_quizzes_by_category(request, category_name, page):
    try:
        retrieved_category = Category.objects.get(title=category_name.title())
        quiz_list = Quiz.objects.filter(
            category=retrieved_category.pk)
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
    serializer = QuizDetailSerializer(paginated_quizzes, many=True)
    if serializer is not None:
        return Response(serializer.data, status=status.HTTP_200_OK)
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
    serializer = QuizDetailSerializer(paginated_quizzes, many=True)
    if serializer is not None:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


# Used to retrieve a quiz by id
def get_quiz_object(pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
        return quiz
    except Quiz.DoesNotExist:
        raise Exception('Quiz with id does not exist')


class RetrieveQuizByIdView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk):
        quiz = get_quiz_object(pk)

        # Increment view count for quiz
        quiz.view_count += 1
        quiz.save()

        serializer = QuizDetailSerializer(quiz, many=False)
        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class RetrieveQuizByTitleView(views.APIView):
    serializer_class = QuizGetByTitleSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            data = request.data
            title = data['title']
            quiz = Quiz.objects.get(title__icontains=title)
        except Quiz.DoesNotExist:
            raise Exception('Quiz with title does not exist')

        serializer = self.serializer_class(quiz, many=False)
        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CreateQuizView(generics.CreateAPIView):
    serializer_class = CreateQuizSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateDestroyQuizView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = CreateQuizSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        quiz = get_quiz_object(pk)
        if quiz is not None:
            serializer = QuizDetailSerializer(quiz, data=request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        quiz = get_quiz_object(pk)
        if quiz is not None:
            serializer = QuizDetailSerializer(quiz, data=request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
