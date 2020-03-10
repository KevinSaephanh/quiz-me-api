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
        validators=[MinLengthValidator(1)], max_length=50, null=False)
    description = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quizzes", blank=True, null=False
    )
    question = models.TextField(
        validators=[MinLengthValidator(1)], max_length=250, blank=True, null=False)
    answer = models.TextField(
        validators=[MinLengthValidator(1)], max_length=250, blank=True, null=False)
    explanation = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.question


class Vote(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, blank=True, null=False)
    user_vote = models.BooleanField()
