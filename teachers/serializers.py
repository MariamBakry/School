from rest_framework import serializers
from .models import Teacher
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer

class TeacherSignupSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = ('user', 'cv', 'password', 'password2')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        
        user_data['password'] = password
        user_data['is_active'] = False
        user_data['user_type'] = 'teacher'

        user = CustomUser.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher