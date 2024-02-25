from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default ='admin')
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES, null = True)
    date_of_birth = models.DateField(null = True)

    class Meta:
        db_table = 'auth_user'
