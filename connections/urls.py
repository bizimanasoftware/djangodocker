# connections/urls.py
from django.urls import path
from . import views

app_name = 'connections' # <--- This is the crucial namespace

urlpatterns = [
    path('', views.connections_list, name='connections_list'), # Matches 'connections_list'
    # Add other URLs for managing connections (e.g., connect, disconnect)
    # path('connect/<int:user_id>/', views.connect_user, name='connect_user'),
    # path('disconnect/<int:user_id>/', views.disconnect_user, name='disconnect_user'),
]
