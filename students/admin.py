from django.contrib import admin
from .models import Student
from django.http import HttpResponse
import csv
from django import forms
from django.urls import path
from django.shortcuts import render
from .serializers import StudentSerializer
from rest_framework.response import Response


class StudentImportForm(forms.Form):
    file = forms.FileField()

class StudentAdmin(admin.ModelAdmin):
    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    def user_gender(self, obj):
        return obj.user.gender

    def user_date_of_birth(self, obj):
        return obj.user.date_of_birth

    list_display = ['user_username', 'user_email', 'user_first_name', 'user_last_name', 'user_gender', 'user_date_of_birth']

    actions = ['export_students']

    
    def export_students(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow(['UserName', 'Email', 'First Name', 'Last Name', 'Gender', 'Date of birth'])
        for student in queryset:
            writer.writerow([student.user.username, student.user.email, student.user.first_name, student.user.last_name, student.user.gender, student.user.date_of_birth])

        return response

    export_students.short_description = "Export selected students to CSV"

admin.site.register(Student, StudentAdmin)
