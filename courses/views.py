from django.shortcuts import get_object_or_404
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
class GetCourseView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        course = get_object_or_404(Course ,pk=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
# class CreateCourseView(APIView):
#     def post(self, request):
#         serializer = CourseSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
# class UpdateCourseView(APIView):
#     def put(self, request, course_id):
#         course = get_object_or_404(Course, pk=course_id)
#         serializer = CourseSerializer(course, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

    
# class DeleteCourseView(APIView):
#     def delete(self, request, course_id):
#         course = get_object_or_404(Course, pk=course_id)
#         course.delete()
#         return Response({'message': 'Course deleted successfully'})
    
