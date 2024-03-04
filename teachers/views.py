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
from rest_framework import status

# Create your views here.

class TeacherSignupView(APIView):
    def post(self, request):
        """
            Creates a new user account of type student.

            Returns:
                A Response object with the new user's data.
        """
        serializer = TeacherSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentsEnrollMyCourseView(APIView):
    """
    API view for teachers to retrieve a paginated list of students enrolled in their course.

    Requires user authentication using the `IsAuthenticated` permission class.
    Uses custom pagination implemented in `CustomCursorPagination`.

    **GET:**
        - Fetches the authenticated user.
        - Checks if the user is of type 'teacher'.
        - Retrieves the teacher object if the user is a teacher.
        - Gets the course object based on the provided ID.
        - Verifies if the retrieved course belongs to the current teacher.
        - If the course is valid:
            - Retrieves enrolled students in the course.
            - Extracts student user primary keys from the enrollments.
            - Fetches all users corresponding to those primary keys.
            - Paginates the results using the specified paginator class.
            - Serializes the paginated students using `CustomUserSerializer`.
            - Returns a paginated response containing the enrolled students.
        - Returns an error response if the user is not the course teacher.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

    def get(self, request, course_id):
        user = request.user
        if user.user_type == 'teacher':
            teacher = user.teacher
            course = get_object_or_404(Course, pk=course_id)
            if course.teacher == teacher:
                enrollments = Enrollment.objects.filter(course=course_id)
                student_user_pks = enrollments.values_list('student__user_id', flat=True)
                all_users = CustomUser.objects.filter(pk__in=student_user_pks)

                paginator = self.pagination_class()
                paginated_students = paginator.paginate_queryset(all_users, request)
                serializer = CustomUserSerializer(paginated_students, many=True)
                return paginator.get_paginated_response(serializer.data)

            return Response({'message': 'You are not the teacher of this course.'})
        return Response({'message': 'it might be you are not a user of type teacher.'})

class CoursesHistoryListView(APIView):
    """
    API view for teachers to retrieve a list of their courses history.

    Requires user authentication using the `IsAuthenticated` permission class.

    **GET:**
        - Fetches the authenticated user.
        - Checks if the user is of type 'teacher'.
        - Retrieves the teacher object if the user is a teacher.
        - Retrieves all courses taught by the teacher (active and not active courses).
        - Serializes the retrieved courses using `CourseSerializer`.
        - Returns the serialized course data.
        - Returns an error response if the user is not a teacher.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type == 'teacher':
            teacher = user.teacher
            courses = Course.objects.filter(teacher=teacher)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        return Response({'message': 'it might be you are not a user of type teacher.'})
