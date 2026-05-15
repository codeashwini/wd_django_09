from django.contrib import admin
from notifications.models import NotificationModel
# Register your models here.
class NotificationAdmin(admin.ModelAdmin):

    list_display = ['notification_title', 'notification_desc', 'notification_slug']

admin.site.register(NotificationModel, NotificationAdmin)