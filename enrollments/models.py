from django.db import models
from students.models import Student
from courses.models import Course

# Create your models here.

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
    class Meta:
        unique_together = [['student', 'course']]