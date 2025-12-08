from django.urls import path
from . import views

urlpatterns = [
    #Default Dash
    path('', views.dashboard, name='supervisor_dashboard'),

    # Management
    path('students/', views.supervisor_students, name='supervisor_students'),
    path('timesheets/modify/<placement_id>', views.supervisor_timesheets_modify, name='supervisor_timesheets_modify'),
    path('timesheets/view/<placement_id>', views.supervisor_timesheets_view, name='supervisor_timesheets_view'),

    # Announcements
    path('announcements/create/', views.supervisor_ann_create, name='supervisor_ann_create'),
    path('announcements/view/', views.supervisor_ann_list, name='supervisor_ann_view'),
    path('announcements/delete/<int:pk>/', views.supervisor_ann_delete, name='supervisor_ann_delete'),
]
