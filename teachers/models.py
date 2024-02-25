from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    cv = models.FileField(upload_to='teachers/cvs', null=True, blank=True)

    def __str__(self):
        return self.user.username