from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.StudentSignupView.as_view(), name='student_signup'),
]
