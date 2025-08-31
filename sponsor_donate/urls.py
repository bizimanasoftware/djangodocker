from django.urls import path
from .views import donate, my_donations

app_name = "sponsor_donate"

urlpatterns = [
    path('donate/', donate, name="donate"),
    path('my-donations/', my_donations, name="my_donations"),
]
