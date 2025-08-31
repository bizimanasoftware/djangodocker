from django.urls import path
from .views import dashboard_view

app_name = 'agents'  # important for namespacing

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
]

