from django.contrib import admin

# Register your models here.
# notifications/admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
