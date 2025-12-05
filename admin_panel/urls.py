from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),

    # User Management
    path('users/add/', views.admin_user_add, name='admin_user_add'),
    path('users/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('users/delete/', views.admin_user_delete, name='admin_user_delete'),

    # Class Management
    path('classes/create/', views.admin_class_create, name='admin_class_create'),
    path('classes/edit/', views.admin_class_edit, name='admin_class_edit'),
    path('classes/delete/', views.admin_class_delete, name='admin_class_delete'),

    # OJT Management
    path('ojt/placements/', views.admin_ojt_placements, name='admin_ojt_placements'),
]
