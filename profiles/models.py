from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)
    is_admin = models.BooleanField(default=False)
    bio = models.TextField(max_length=250, blank=True, null=True)
    profile_pic = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
