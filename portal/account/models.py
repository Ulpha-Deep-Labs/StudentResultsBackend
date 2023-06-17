from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    role = models.CharField(null=True, blank=True, max_length=100)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


