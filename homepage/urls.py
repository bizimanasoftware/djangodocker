from django.urls import path
from . import views
from django.views.generic import TemplateView # Make sure this is imported
app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('become-agent/', views.become_agent, name='become_agent'),
    path('become-talent/', views.become_talent, name='become_talent'),
    path('sponsor-donate/', views.sponsor_donate, name='sponsor_donate'),
    path('terms/', TemplateView.as_view(template_name='homepage/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='homepage/privacy.html'), name='privacy'),
]
