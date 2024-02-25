from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:course_id>/', views.GetCourseView.as_view(), name='course_detail'),
    # path('create/', views.CreateCourseView.as_view(), name='create_course'),
    # path('<int:course_id>/update/', views.UpdateCourseView.as_view(), name='update_course'),
    # path('<int:course_id>/delete/', views.DeleteCourseView.as_view(), name='delete_course'),
]
