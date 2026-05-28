from django.db import models

# Create your models here.
class RegUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    course = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    confirm_pass = models.CharField(max_length=10)
    terms = models.CharField(max_length=10)
    reset_token = models.CharField(max_length=100, null=True, blank=True)