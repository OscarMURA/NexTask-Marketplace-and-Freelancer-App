# Comments/admin.py

from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('task__title', 'author__username', 'content')
    list_filter = ('created_at',)
