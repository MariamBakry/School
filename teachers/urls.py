from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.TeacherSignupView.as_view(), name='teacher_signup'),
    path('<int:course_id>/students/', views.StudentsEnrollMyCourseView.as_view(), name='students_enroll_course'),
    path('history/', views.CoursesHistoryListView.as_view(), name='corses_history'),
]
