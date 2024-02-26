from django.contrib import admin
from .models import Course
# Register your models here.

""" Check if the teacher is already assigned to a course within
    the same time frame """
class CourseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """get all courses of the same teacher and the same time frame
            of the current course, with excluding the current course"""
        existing_courses = Course.objects.filter(
            teacher=obj.teacher,
            start_date__lte=obj.end_date,
            end_date__gte=obj.start_date
        ).exclude(pk=obj.pk)
        
        if existing_courses.exists():
            conflicting_courses = ", ".join([course.name for course in existing_courses])
            message = f"The teacher is already assigned to the following course(s) during this time period: {conflicting_courses}"
            self.message_user(request, message, level='ERROR')
            return
        
        super().save_model(request, obj, form, change)

admin.site.register(Course, CourseAdmin)