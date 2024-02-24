from django.db import models
from django.utils import timezone

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)
    # teacher_id = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(default = timezone.now().date())
    end_date = models.DateField(default = timezone.now().date())
    active = models.BooleanField(default=False)

    
