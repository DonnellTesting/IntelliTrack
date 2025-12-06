# student/models.py
from django.db import models
from accounts.models import User
import datetime

CURRENT_YEAR = datetime.date.today().year
YEAR_CHOICES = [(y, f"Class of {y}") for y in range(CURRENT_YEAR-5, CURRENT_YEAR+5)]

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

    batch_year = models.IntegerField(
        choices=YEAR_CHOICES,
        null=True,
        blank=True
    )

    batch_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    target_hours = models.IntegerField(default=600)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.company_name or 'No company yet'}"


class OJTProgress(models.Model):
    ojt = models.ForeignKey(
        OJTPlacement,
        on_delete=models.CASCADE,
        related_name="progress_entries"
    )

    date = models.DateField()

    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    performance_rating = models.IntegerField(default=0)  # 1–10 rating

    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('ojt', 'date')  # One entry per day

    def __str__(self):
        return f"{self.ojt.student.get_full_name()} - {self.date}"
