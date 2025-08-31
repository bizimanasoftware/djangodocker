# emails/urls.py

from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    # This is the webhook URL you give to SMTP2GO
    path('incoming/', views.incoming_email_webhook, name='incoming_webhook'),
]
