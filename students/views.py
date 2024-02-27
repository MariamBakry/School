from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
# Create your views here.

class StudentSignupView(APIView):
    def post(self, request):
        """
            Creates a new user account of type student.

            Returns:
                A Response object with the new user's data.
        """
        serializer = StudentSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)