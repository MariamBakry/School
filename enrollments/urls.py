from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.EnrollmentListView.as_view(), name='student_enrollments'),
    path('new-enroll/', views.EnrollCourseView.as_view(), name='enroll_course'),
    path('leave-course/', views.LeaveCourseView.as_view(), name='leave_course'),
]
