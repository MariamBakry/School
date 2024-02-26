# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer, NewEnrollSerializer
from courses.models import Course
import datetime
# Create your views here.

class EnrollmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user.student
        enrollments = Enrollment.objects.filter(student = student)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = request.user.student
        data = request.data.copy()
        data['student'] = student

        course_name = data.pop('course_name')
        course_name = str(course_name[0])

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response({'error': f"Course '{course_name}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if course.start_date > datetime.date.today():
            data['course'] = course.id

            serializer = NewEnrollSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You can not Enroll the Course after the course start date.'})
    

class LeaveCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = request.user.student
        data = request.data.copy()
        data['student'] = student

        course_name = data.pop('course_name')
        course_name = str(course_name[0])

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response({'error': f"Course '{course_name}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            enrollment = Enrollment.objects.get(student=student, course=course)
        except Enrollment.DoesNotExist:
            return Response({'error': 'You are not enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
        
        if course.start_date > datetime.date.today():
            data['course'] = course.id

            enrollment.delete()
            return Response({'message': 'You have successfully left the course'}, status=status.HTTP_200_OK)
        return Response({'message': 'You can not Leave the Course after the course start date.'})