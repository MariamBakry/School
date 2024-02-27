from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from courses.models import Course
from enrollments.models import Enrollment
from students.models import Student
from courses.serializers import CourseSerializer
from school.pagination import CustomCursorPagination

# Create your views here.

class TeacherSignupView(APIView):
    def post(self, request):
        serializer = TeacherSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class StudentsEnrollMyCourseView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

    def get(self, request, course_id):
        user = request.user
        if user.user_type == 'teacher':
            teacher = user.teacher
            course = get_object_or_404(Course, pk=course_id)
            if course.teacher == teacher:
                enrollments = Enrollment.objects.filter(course=course_id)
                students = []
                for enrollment in enrollments:
                    students.append(enrollment.student)
                all_students = Student.objects.filter(pk__in=students)
                all_users = []

                for student in all_students:
                    all_users.append(student.user.pk)
                all_users = CustomUser.objects.filter(pk__in=all_users)

                paginator = self.pagination_class()
                paginated_students = paginator.paginate_queryset(all_users, request)
                serializer = CustomUserSerializer(paginated_students, many=True)
                return paginator.get_paginated_response(serializer.data)

            return Response({'message': 'You are not the teacher of this course.'})
        return Response({'message': 'it might be you are not a user of type teacher.'})

class CoursesHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type == 'teacher':
            teacher = user.teacher
            courses = Course.objects.filter(teacher=teacher)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        return Response({'message': 'it might be you are not a user of type teacher.'})
