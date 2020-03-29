from django.db import models
from django.core.validators import MinLengthValidator
from pip._vendor.pyparsing import re
from users.models import CustomUser


class Category(models.Model):
    title = models.CharField(
        validators=[MinLengthValidator(1)], max_length=30, unique=True, null=False)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    title = models.CharField(
        validators=[MinLengthValidator(5)], max_length=50, null=False, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category")
    created_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_questions(self):
        questions = Question.objects.filter(quiz=self)
        return questions

    def get_votes(self):
        votes = Vote.objects.filter(quiz=self)
        return votes


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quizzes", blank=True, null=True
    )
    question = models.TextField(
        validators=[MinLengthValidator(1)], max_length=250, blank=True, null=False)
    answer = models.TextField(
        validators=[MinLengthValidator(1)], max_length=250, blank=True, null=False)

    def __str__(self):
        return self.question


class Vote(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, blank=True, null=False)
    user_vote = models.IntegerField(default=0)
