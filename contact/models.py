from django.db import models

# Create your models here.
class Contact(models.Model):

    email = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip = models.CharField(max_length=10)
    terms = models.CharField(max_length=10)