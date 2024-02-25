from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username