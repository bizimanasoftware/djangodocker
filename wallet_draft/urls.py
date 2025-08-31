# wallet/urls.py
from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    # Wallet Dashboard
    path('dashboard/', views.wallet_dashboard, name='wallet_dashboard'),

    # Deposit Flows
    path('deposit/', views.deposit_method_selection, name='deposit_method_selection'),
    path('deposit/crypto/', views.crypto_deposit_request, name='crypto_deposit_request'),
    path('deposit/crypto/details/<uuid:transaction_id>/', views.crypto_deposit_details, name='crypto_deposit_details'),
    path('deposit/p2p/', views.p2p_deposit_request, name='p2p_deposit_request'),
    path('deposit/p2p/details/<uuid:transaction_id>/', views.p2p_deposit_details, name='p2p_deposit_details'),
    path('deposit/p2p/upload-proof/<uuid:transaction_id>/', views.p2p_deposit_upload_proof, name='p2p_deposit_upload_proof'),

    # Withdrawal Flows
    path('withdraw/', views.withdrawal_method_selection, name='withdrawal_method_selection'),
    path('withdraw/crypto/', views.crypto_withdrawal_request, name='crypto_withdrawal_request'),
    path('withdraw/p2p/', views.p2p_withdrawal_request, name='p2p_withdrawal_request'),
    
    # Internal Transfer
    path('transfer/', views.internal_transfer, name='internal_transfer'),

    # Donation Flow
    path('donate/', views.donate, name='donate'),
    path('donate/details/<uuid:transaction_id>/', views.crypto_donation_details, name='crypto_donation_details'),
    path('donate/status/<uuid:transaction_id>/', views.crypto_donation_details, name='donation_status'),
    # Callbacks & IPN
    path('nowpayments-ipn/', views.nowpayments_webhook, name='nowpayments_ipn'),
   # path('deposit/success/', views.deposit_success_callback, name='deposit_success'),
   # path('deposit/fail/', views.deposit_fail_callback, name='deposit_fail'),
    #path('deposit/cancel/', views.deposit_cancel_callback, name='deposit_cancel'),
]
