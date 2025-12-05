from django.db import models
from accounts.models import User

class Class(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'instructor'}
    )
    students = models.ManyToManyField(
        User,
        related_name='student_classes',
        limit_choices_to={'role': 'student'},
        blank=True
    )

    def __str__(self):
        return self.name