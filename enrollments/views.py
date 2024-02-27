from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer, NewEnrollSerializer
from courses.models import Course
import datetime
from school.pagination import CustomCursorPagination
# Create your views here.

class EnrollmentListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

    def get(self, request):
        user = request.user
        if user.user_type == 'student':
            student = user.student
            enrollments = Enrollment.objects.filter(student = student)
            
            paginator = self.pagination_class()
            paginated_enrollments = paginator.paginate_queryset(enrollments, request)
            serializer = EnrollmentSerializer(paginated_enrollments, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response({'message': 'it might be you are not a user of type student.'})
        

class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type == 'student':
            student = user.student
            data = request.data.copy()
            data['student'] = student

            course_name = data.pop('course_name')
            course_name = str(course_name[0])
            course = get_object_or_404(Course, name=course_name)
            
            if course.is_active:
                if course.start_date > datetime.date.today():
                    data['course'] = course.id

                    serializer = NewEnrollSerializer(data = data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'You can not Enroll the Course after the course start date.'})
            return Response({'message': 'This course has not yet been activated by the administrator, so enrollment is currently unavailable.'})  
        return Response({'message': 'it might be you are not a user of type student.'})

class LeaveCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type == 'student':
            student = user.student
            data = request.data.copy()
            data['student'] = student

            course_name = data.pop('course_name')
            course_name = str(course_name[0])
            course = get_object_or_404(Course, name=course_name)
            
            try:
                enrollment = Enrollment.objects.get(student=student, course=course)
            except Enrollment.DoesNotExist:
                return Response({'error': 'You are not enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
            
            if course.start_date > datetime.date.today():
                data['course'] = course.id

                enrollment.delete()
                return Response({'message': 'You have successfully left the course'}, status=status.HTTP_200_OK)
            return Response({'message': 'You can not Leave the Course after the course start date.'})
        return Response({'message': 'it might be you are not a user of type student.'})