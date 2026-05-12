from django.db import models
from tinymce.models import HTMLField
class Courses(models.Model):

    course_icon = models.CharField(max_length=50)
    course_title = models.CharField(max_length=50)
    course_desc = HTMLField()
    course_price = models.CharField(max_length=10)
    course_duration = models.CharField(max_length=10)
    
