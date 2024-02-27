from rest_framework import serializers
from .models import *

class EnrollmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only = True)

    class Meta:
        model = Enrollment
        fields = ['course_name', 'enrollment_date']


class NewEnrollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ['student', 'course']