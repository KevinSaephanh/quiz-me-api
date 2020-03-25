# Generated by Django 3.0.3 on 2020-03-25 19:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_auto_20200318_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]