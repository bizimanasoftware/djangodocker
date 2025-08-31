from django.urls import path
from .views import dashboard_view

app_name = 'filmmakers' # important for namespacing

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
]
