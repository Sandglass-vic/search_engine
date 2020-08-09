from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    gender_choice = (('boy', 'boy'), ('girl', 'girl'))
    gender = models.CharField(max_length=32, choices=gender_choice, default='boy')

    def __str__(self):
        return self.username

