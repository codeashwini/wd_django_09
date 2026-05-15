from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
# Create your models here.
class NotificationModel(models.Model):

    notification_title = models.CharField(max_length=30, default=None)
    notification_slug = AutoSlugField(populate_from='notification_title',unique=True, null=True, default=None)
    notification_desc = HTMLField()

   