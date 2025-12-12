from django.urls import path
from . import views

urlpatterns = [
    #Default Dash
    path('', views.dashboard, name='instructor_dashboard'),

    #Class List
    path('placements/', views.instructor_placements, name='instructor_placements'),

    # OJT Management
    path('timesheets/', views.instructor_timesheets, name='instructor_timesheets'),
    path('timesheets/view/<placement_id>', views.instructor_timesheets_view, name='instructor_timesheets_view'),
    path('timesheets/calendar/<int:placement_id>', views.instructor_timesheets_calendar, name='instructor_timesheets_calendar'),
    path('timesheets/print/<int:placement_id>/', views.instructor_timesheets_print, name='instructor_timesheets_print'),
    path('timesheets/certificate/<int:placement_id>', views.instructor_timesheets_certificate, name='instructor_timesheets_certificate'),

    # Announcements
    path('announcements/create/', views.instructor_announcement_create, name='instructor_announcement_create'),
    path('announcements/view/', views.instructor_announcement_list, name='instructor_announcement_list'),
    path('announcements/delete/<int:pk>/', views.instructor_announcement_delete, name='instructor_announcement_delete'),
]