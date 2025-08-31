# emergencies/urls.py

from django.urls import path
from .views import (
    EmergencyCampaignListView,
    EmergencyCampaignDetailView,
    CreateCampaignRequestView,
    ProcessSponsorMessageView,
    AddCommentView,
    dashboard_view,
    CampaignUpdateView,
    PaymentMethodCreateView,
    PaymentMethodDeleteView,
)

app_name = 'emergencies'

urlpatterns = [
    # Public Views
    path('', EmergencyCampaignListView.as_view(), name='campaign_list'),
    path('campaign/<slug:slug>/', EmergencyCampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/<slug:slug>/contact/', ProcessSponsorMessageView.as_view(), name='process_sponsor_message'),
    path('campaign/<slug:slug>/comment/', AddCommentView.as_view(), name='add_comment'),

    # User-facing Campaign Creation & Management
    path('request/', CreateCampaignRequestView.as_view(), name='create_campaign_request'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/campaign/<slug:slug>/edit/', CampaignUpdateView.as_view(), name='update_campaign'),
    path('dashboard/campaign/<slug:slug>/add-payment/', PaymentMethodCreateView.as_view(), name='add_payment_method'),
    path('dashboard/payment/<int:pk>/delete/', PaymentMethodDeleteView.as_view(), name='delete_payment_method'),
]
