from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(unique = True, max_length = 25)
    password = models.CharField(blank = True, max_length = 250)
    email = models.EmailField(blank = True, unique = True)
    profile_pic = models.ImageField(blank = True, null = True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('guest', 'Guest'),
    )
    role = models.CharField(blank = True, max_length = 25, choices = ROLE_CHOICES, default='member')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.username

