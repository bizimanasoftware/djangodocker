from django.urls import path
from .views import create_ticket

app_name = "support_tickets"

urlpatterns = [
    path('create/', create_ticket, name="create_ticket"),
]
