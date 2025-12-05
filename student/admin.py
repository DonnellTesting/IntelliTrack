from django.contrib import admin
from .models import OJTPlacement

@admin.register(OJTPlacement)
class OJTPlacementAdmin(admin.ModelAdmin):
    list_display = ("student", "supervisor", "company_name", "start_date", "end_date")
    list_filter = ("company_name", "supervisor")
    search_fields = ("student__first_name", "student__last_name", "company_name")