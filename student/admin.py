from django.contrib import admin
from .models import OJTPlacement, OJTProgress

class OJTProgressInline(admin.TabularInline):
    model = OJTProgress
    extra = 1
    fields = ("date", "hours_worked", "performance_rating", "remarks")
    ordering = ("-date",)  # newest entries first


@admin.register(OJTPlacement)
class OJTPlacementAdmin(admin.ModelAdmin):
    list_display = ("student", "supervisor", "company_name", "start_date", "end_date")
    list_filter = ("company_name", "supervisor")
    search_fields = ("student__first_name", "student__last_name", "company_name")

    inlines = [OJTProgressInline]


@admin.register(OJTProgress)
class OJTProgressAdmin(admin.ModelAdmin):
    list_display = ("ojt", "date", "hours_worked", "performance_rating")
    list_filter = ("date", "performance_rating")
    search_fields = ("ojt__student__first_name", "ojt__student__last_name")