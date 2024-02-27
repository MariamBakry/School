from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from school.pagination import CustomCursorPagination
# Create your views here.

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

    def get(self, request):
        courses = Course.objects.filter(is_active=True)

        paginator = self.pagination_class()
        paginated_courses = paginator.paginate_queryset(courses, request)

        serializer = CourseSerializer(paginated_courses, many=True)
        return paginator.get_paginated_response(serializer.data)
