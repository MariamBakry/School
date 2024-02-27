from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import *
from .serializers import *
from rest_framework import generics

class LoginView(APIView):
    """
        Logs in a user and returns refresh and access tokens.

        Returns:
            A Response object with the tokens or an error message.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.user_type == 'Admin':
                return Response({'error': 'Admin users cannot log in'}, status=status.HTTP_403_FORBIDDEN)
            
            login(request, user)
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    """
        Logs out the current user.

        Returns:
            A Response object with a success message.
    """
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

    
class UserProfileView(generics.RetrieveAPIView):
    """
    Retrieves the current user's profile.

    Returns:
        A Response object with the user's profile data.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
    
class UpdateUserProfileView(generics.UpdateAPIView):
    """
        Updates the current user's profile.

        Returns:
            A Response object with the updated user's profile data.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user
    
class Signup(APIView):
    def match_passwords(self,validated_data):
        """
            Validates that the two password fields match.

            Raises:
                ValidationError: If the passwords do not match.

            Returns:
                The password to the SignupView in teacher or student serializers.
        """
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return password