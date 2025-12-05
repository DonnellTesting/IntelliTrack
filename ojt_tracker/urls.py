from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts handles login, logout, register, etc
    path('', include('accounts.urls')),

    # dashboard modules
    path('student/', include('student.urls')),
    path('instructor/', include('teacher.urls')),
    path('supervisor/', include('companies.urls')),
    path('admin-dashboard/', include('admin_panel.urls')),
]
