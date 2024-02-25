from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True},
        }