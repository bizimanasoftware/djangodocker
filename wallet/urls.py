# wallet/urls.py (UPDATED FOR DIRECT CRYPTO SPONSORSHIP)
from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    # Main Dashboard
    path('dashboard/', views.wallet_dashboard, name='wallet_dashboard'),
    
    # --- Sponsorship URLs ---
    # Original, manual sponsorship form
    path('sponsor-manual/<str:recipient_username>/', views.create_sponsorship_deposit, name='create_sponsorship_deposit'),
    # New, direct crypto sponsorship form
    path('sponsor-crypto/<str:recipient_username>/', views.create_crypto_sponsorship, name='create_crypto_sponsorship'),

    # Deposit URLs
    path('deposit/crypto/', views.crypto_deposit_request, name='crypto_deposit_request'),
    path('deposit/p2p/', views.p2p_deposit_request, name='p2p_deposit_request'),
    path('deposit/p2p/<uuid:transaction_id>/upload-proof/', views.p2p_deposit_upload_proof, name='p2p_deposit_upload_proof'),
    
    # Transfer URL
    path('transfer/', views.internal_transfer, name='internal_transfer'),
    
    # Withdrawal URLs
    path('withdrawal/crypto/', views.crypto_withdrawal_request, name='crypto_withdrawal_request'),
    path('withdrawal/p2p/', views.p2p_withdrawal_request, name='p2p_withdrawal_request'),

    # NOWPayments Callbacks (used by both crypto deposit and crypto sponsorship)
    path('nowpayments-ipn/', views.nowpayments_ipn, name='nowpayments_ipn'),
    path('deposit-success/', views.deposit_success_callback, name='deposit_success_callback'),
    path('deposit-cancel/', views.deposit_cancel_callback, name='deposit_cancel_callback'),
    
    # Standalone Donation View
    path('donate/', views.donation_view, name='donate'),

    # AJAX endpoint
    path('ajax/get-minimum-amount/', views.get_minimum_amount_api, name='get_minimum_amount_api'),
]
