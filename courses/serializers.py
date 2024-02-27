from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField(source='teacher.user.username', read_only = True)
    class Meta:
        model = Course
        fields = ['name', 'teacher_username', 'description', 'start_date', 'end_date', 'is_active']