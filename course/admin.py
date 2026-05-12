from django.contrib import admin
from course.models import Courses
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_icon','course_title', 'course_desc', 'course_price', 'course_duration']

admin.site.register(Courses, CourseAdmin)