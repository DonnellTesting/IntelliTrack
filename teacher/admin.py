from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor')
    filter_horizontal = ('students',)  # Makes M2M selection nicer
