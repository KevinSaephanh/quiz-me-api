from rest_framework import serializers
from .models import Category, Question, Quiz
from users.models import CustomUser
from django.db import IntegrityError, transaction


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question', 'answer', 'explanation']
        read_only_fields = ['quiz']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(source='get_questions', many=True)
    creator = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)

    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['created_at', 'creator']


class CreateQuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    creator = serializers.CharField(max_length=15)
    category = serializers.CharField(max_length=30)

    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['created_at']

    def create(self, request):
        data = request.data
        creator = CustomUser.objects.get(username=data['creator'])
        category = Category.objects.get(title=format_word(data['category']))

        # save quiz
        quiz = Quiz()
        quiz.creator = creator
        quiz.title = data['title']
        quiz.description = data['description']
        quiz.category = category

        # Atomic transaction to save quiz and questions or roll back
        try:
            with transaction.atomic():
                quiz.save()

                # Create question set
                for q in data['questions']:
                    question = Question()
                    question.quiz = quiz
                    question.question = q['question']
                    question.answer = q['answer']
                    question.save()
        except IntegrityError:
            raise Exception('Failed to save all questions')
        return quiz


class QuizGetByTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        write_only_fields = ['title']
        read_only_fields = ['description', 'creator', 'category', 'pk']


def format_word(word):
    formatted_word = word.lower().title()
    return formatted_word
