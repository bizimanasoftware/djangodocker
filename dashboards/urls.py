from django.urls import path
from .views import dashboard_redirect_view
app_name: 'dashboards'
urlpatterns = [
    # This is the URL that LOGIN_REDIRECT_URL points to.
    path('', dashboard_redirect_view, name='redirect'),
]
