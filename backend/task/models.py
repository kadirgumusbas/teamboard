from django.db import models
from project.models import Project
from root.settings import AUTH_USER_MODEL
from team.models import Team
from user.models import CustomUser


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task_project')
    assignee = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_assignee', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

