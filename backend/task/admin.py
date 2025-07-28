from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'project', 'assignee', 'status', 'due_date', 'created_at']
    list_filter = ['project', 'status', 'assignee']
    search_fields = ['title', 'description']
