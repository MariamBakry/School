from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from school.pagination import CustomCursorPagination
# Create your views here.

class CourseListView(APIView):
    """
        API view for retrieving a paginated list of active courses.

        Requires user authentication using the `IsAuthenticated` permission class.
        Uses custom pagination implemented in `CustomCursorPagination`.

        **GET:**
            - Retrieves all active courses (`is_active=True`).
            - Paginates the results using the specified paginator class.
            - Serializes the paginated data using `CourseSerializer`.
            - Returns a paginated response object.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

    def get(self, request):
        courses = Course.objects.filter(is_active=True)

        paginator = self.pagination_class()
        paginated_courses = paginator.paginate_queryset(courses, request)

        serializer = CourseSerializer(paginated_courses, many=True)
        return paginator.get_paginated_response(serializer.data)
