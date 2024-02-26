from django.db import models
from django.utils import timezone
from teachers.models import Teacher

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    start_date = models.DateField(default = timezone.now().date())
    end_date = models.DateField(default = timezone.now().date())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    
