from rest_framework import serializers
from .models import Student
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from accounts.views import Signup

class StudentSignupSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ('user', 'password', 'password2')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = Signup.match_passwords(self, validated_data)
        
        user_data['password'] = password
        user_data['is_active'] = False
        user_data['user_type'] = 'student'

        user = CustomUser.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student
    
    
class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Student
        fields = ['id', 'username']