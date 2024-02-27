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
    """
    API view for retrieving a paginated list of a student's enrollments.

    Requires user authentication using the `IsAuthenticated` permission class.
    Uses custom pagination implemented in `CustomCursorPagination`.

    **GET:**
        - Fetches the authenticated user.
        - Checks if the user is of type 'student'.
        - If the user is a student, retrieves their enrollments.
        - Paginates the results using the specified paginator class.
        - Serializes the paginated data using `EnrollmentSerializer`.
        - Returns a paginated response object containing the enrollments,
          or an error message if the user is not a student.
    """
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
        

def check_active_course_for_enroll(self, course_name):
    """
    Checks if a course is available for enrollment based on its status and start date.

    Returns:
        The course object if it's active and has a future start date, otherwise None.
    """
    course_name = str(course_name[0])
    course = get_object_or_404(Course, name=course_name)
    if not course.is_active:
        return None
    if course.start_date <= datetime.date.today():
        return None
    return course

class EnrollCourseView(APIView):
    """
    API view for enrolling students in courses.

    Requires user authentication using the `IsAuthenticated` permission class.

    **POST:**
        - Fetches the authenticated user.
        - Checks if the user is of type 'student'.
        - Retrieves the student object.
        - Extracts the course name from the request data.
        - Calls `check_active_course_for_enroll` to ensure the course is valid.
        - If the course is valid, sets the course ID in the data and serializes.
        - Saves the enrollment on successful validation and returns a created response.
        - Returns a bad request response if enrollment validation fails.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'student':
            return Response({'message': 'it might be you are not a user of type student.'})
        student = user.student
        data = request.data.copy()
        data['student'] = student

        course_name = data.pop('course_name')
        course = check_active_course_for_enroll(self, course_name)
        if course is None:
            return Response({'message': 'Course is not available for enrollment.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['course'] = course.id
        serializer = NewEnrollSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LeaveCourseView(APIView):
    """
    API view for leaving students a courses.

    Requires user authentication using the `IsAuthenticated` permission class.

    **POST:**
        - Fetches the authenticated user.
        - Checks if the user is of type 'student'.
        - Retrieves the student object.
        - Extracts the course name from the request data.
        - Calls `check_active_course_for_enroll` to ensure the course is valid.
        - If the course is valid, sets the course ID in the data and serializes.
        - Saves the enrollment on successful validation and returns a success leaving response.
        - Returns a bad request response if enrollment validation fails.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'student':
            return Response({'message': 'it might be you are not a user of type student.'})
        student = user.student
        data = request.data.copy()
        data['student'] = student

        course_name = data.pop('course_name')
        course = check_active_course_for_enroll(self, course_name)
        if course is None:
            return Response({'message': 'Course is not available for Leaving.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['course'] = course.id
        
        try:
            enrollment = Enrollment.objects.get(student=student, course=course)
        except Enrollment.DoesNotExist:
            return Response({'error': 'You are not enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
        
        enrollment.delete()
        return Response({'message': 'You have successfully left the course'}, status=status.HTTP_200_OK)
        