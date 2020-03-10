from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField(
        validators=[MinLengthValidator(3), RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Username must be Alphanumeric',
            code='invalid_username'
        )], max_length=15, blank=True, null=False, unique=True)
    email = models.EmailField(
        max_length=50, blank=True, null=False, unique=True)
    password = models.CharField(
        validators=[MinLengthValidator(7), RegexValidator(
            regex='^(?=.*?[A-Z]).*\d',
            message='Password must have at least one number and one uppercase letter',
            code='invalid_password'
        )], max_length=70, blank=True, null=False)
    bio = models.TextField(max_length=250, blank=True, null=True)
    profile_pic = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
