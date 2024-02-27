from rest_framework import serializers
from .models import Teacher
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from accounts.views import Signup

class TeacherSignupSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = ('user', 'cv', 'password', 'password2')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = Signup.match_passwords(self, validated_data)
        
        user_data['password'] = password
        user_data['is_active'] = False
        user_data['user_type'] = 'teacher'

        user = CustomUser.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher