from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.EnrollmentListView.as_view(), name='student_enrollments'),
    path('newenroll/', views.EnrollCourseView.as_view(), name='enroll_course'),
    path('leavecourse/', views.LeaveCourseView.as_view(), name='leave_course'),
]
