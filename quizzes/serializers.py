from rest_framework import serializers
from .models import Category, Question, Quiz, Vote
from django.contrib.auth.models import User


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class QuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    creator = StringSerializer(many=False)
    category = StringSerializer(many=False)
    votes = serializers.SerializerMethodField()

    def check_question_set_size(self):
        if self.questions_set.count() > 250:
            raise Exception('Cannot exceed 1000 questions per quiz')
        return True

    def get_questions(self):
        return self.question_set.all()

    def get_votes(self):
        return self.vote_set.all()

    def create(self, request):
        data = request.data
        creator = User.objects.get(username=data['creator'])

        # Create new quiz
        quiz = Quiz()
        quiz.creator = creator
        quiz.title = data['title']
        quiz.description = data['description']
        quiz.category = data['category']
        quiz.save()

        # Create question set
        for q in data['questions']:
            question = Question()
            question.quiz = quiz
            question.question = q['question']
            question.answer = q['answer']
            question.explanation = q['explanation']
            question.save()
        return quiz

    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['creator', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['quiz']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ['quiz', 'user']
