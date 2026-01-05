from django.contrib import admin
from django import forms
from .models import OJTPlacement, OJTProgress

class OJTProgressInline(admin.TabularInline):
    model = OJTProgress
    extra = 1
    fields = ("date", "hours_worked", "performance_rating", "remarks")
    ordering = ("-date",)  # newest entries first


class OJTPlacementForm(forms.ModelForm):
    schedule_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
    )

    class Meta:
        model = OJTPlacement
        fields = '__all__'  # includes phone_number now

@admin.register(OJTPlacement)
class OJTPlacementAdmin(admin.ModelAdmin):
    form = OJTPlacementForm
    list_display = (
        "student", "supervisor", "company_name",
        "start_date", "end_date", "schedule_days", "schedule_time"
    )
    readonly_fields = ('batch_year',)


@admin.register(OJTProgress)
class OJTProgressAdmin(admin.ModelAdmin):
    list_display = ("ojt", "date", "hours_worked", "performance_rating")
    list_filter = ("date", "performance_rating")
    search_fields = (
        "placement__student__first_name",
        "placement__student__last_name",
        "placement__company_name",
    )

    def ojt(self, obj):
        """Return the placement field, but labeled as 'OJT' in the admin."""
        return obj.placement

    ojt.short_description = "OJT Placement"