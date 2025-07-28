from django.db import models

from root.settings import AUTH_USER_MODEL


class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_owner')
    members = models.ManyToManyField(AUTH_USER_MODEL, related_name='team_members')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
