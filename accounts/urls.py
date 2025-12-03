from django.urls import path
from .views import landing_page

urlpatterns = [
    path('', landing_page, name='landing-page'),  # root of the app
]
