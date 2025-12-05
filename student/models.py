# student/models.py
from django.db import models
from accounts.models import User

class OJTPlacement(models.Model):
    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='ojt_placement',
        limit_choices_to={'role': 'student'}
    )

    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_students',
        limit_choices_to={'role': 'company'}
    )

    company_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    target_hours = models.IntegerField(default=600)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.company_name or 'No company yet'}"