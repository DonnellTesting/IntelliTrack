from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Announcement

class CustomUserAdmin(UserAdmin):
    # Add your custom field `role` to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

admin.site.register(User, CustomUserAdmin)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "visible_to_all")
    search_fields = ("title", "content", "author__username")
    list_filter = ("visible_to_all", "created_at")
