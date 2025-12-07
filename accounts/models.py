from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('company', 'Company Supervisor'),
        ('admin', 'Administrator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Announcement(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="announcements"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # For future expansion (instructors, supervisors posting)
    visible_to_all = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.author.username})"
