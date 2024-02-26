from django.db import models
from django.utils import timezone
from teachers.models import Teacher
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.

def validate_end_date_greater_than_start_date(value):
    if value.end_date <= value.start_date:
        raise ValidationError('End date must be greater than the start date.')


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    start_date = models.DateField(default = timezone.now().date())
    end_date = models.DateField(default = timezone.now().date())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        validate_end_date_greater_than_start_date(self)
        return super().clean()
    
