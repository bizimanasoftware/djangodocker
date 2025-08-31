# wallet/views.py (UPDATED FOR DIRECT CRYPTO SPONSORSHIP)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db import transaction as db_transaction
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from decimal import Decimal
from django.contrib.auth import get_user_model

import requests
import json
import uuid
import hmac
import hashlib
import time

from .models import Wallet, Transaction
from .forms import (
    SponsorshipDepositForm,
    CryptoSponsorshipForm, # NEW
    CryptoDepositForm, P2PDepositRequestForm, ProofOfPaymentUploadForm,
    InternalTransferForm, CryptoWithdrawalForm,
    P2PWithdrawalRequestForm
)

User = get_user_model()

# NOWPayments API configuration
NOWPAYMENTS_API_KEY = getattr(settings, 'NOWPAYMENTS_API_KEY', None)
NOWPAYMENTS_IPN_SECRET = getattr(settings, 'NOWPAYMENTS_IPN_SECRET', None)
NOWPAYMENTS_BASE_URL = getattr(settings, 'NOWPAYMENTS_BASE_URL', 'https://api.nowpayments.io/v1')


# --- NEW: DIRECT CRYPTO SPONSORSHIP VIEW ---
def create_crypto_sponsorship(request, recipient_username):
    """
    Public view for anyone to sponsor a user with crypto via NOWPayments.
    """
    try:
        recipient = User.objects.select_related('wallet').get(username=recipient_username)
        recipient_wallet = recipient.wallet
    except (User.DoesNotExist, Wallet.DoesNotExist):
        messages.error(request, "The user you are trying to sponsor does not exist or does not have an active wallet.")
        return redirect('/')

    if request.method == 'POST':
        form = CryptoSponsorshipForm(request.POST, user=request.user)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            crypto_currency_api_code = form.cleaned_data['crypto_currency']

            # Create a unique order ID for tracking
            order_id = f"sponsor_{recipient.id}_{int(time.time())}"

            headers = {'x-api-key': NOWPAYMENTS_API_KEY, 'Content-Type': 'application/json'}
            payload = {
                "price_amount": str(amount),
                "price_currency": "usd",
                "pay_currency": crypto_currency_api_code,
                "ipn_callback_url": request.build_absolute_uri(reverse('wallet:nowpayments_ipn')),
                "order_id": order_id,
                "success_url": request.build_absolute_uri(reverse('wallet:deposit_success_callback')),
                "cancel_url": request.build_absolute_uri(reverse('wallet:deposit_cancel_callback')),
            }

            try:
                response = requests.post(f"{NOWPAYMENTS_BASE_URL}/payment", headers=headers, json=payload)
                response.raise_for_status()
                nowpayments_data = response.json()

                if nowpayments_data.get('payment_id'):
                    with db_transaction.atomic():
                        # Create the trackable transaction record
                        transaction = form.save(commit=False)
                        transaction.wallet = recipient_wallet
                        transaction.transaction_type = 'sponsorship_crypto'
                        transaction.status = 'pending'
                        transaction.nowpayments_payment_id = nowpayments_data['payment_id']

                        # Assign sponsor details
                        if request.user.is_authenticated:
                            transaction.sponsor = request.user
                        # Guest details are already on the form instance

                        # Create a clear description
                        desc = f"Crypto sponsorship for {recipient.username}. "
                        if form.cleaned_data.get('description'):
                            desc += f"Message: '{form.cleaned_data.get('description')}'"
                        transaction.description = desc
                        transaction.save()

                    # Redirect user to NOWPayments payment page
                    return render(request, 'wallet/crypto_deposit_details.html', {'nowpayments_data': nowpayments_data})
                else:
                    messages.error(request, "Could not initiate payment with NOWPayments. Please try again.")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"Error connecting to payment provider: {e}")

    else:
        form = CryptoSponsorshipForm(user=request.user)

    context = {
        'form': form,
        'recipient': recipient,
    }
    return render(request, 'wallet/crypto_sponsorship_form.html', context)


# --- EXISTING MANUAL SPONSORSHIP VIEW (Unchanged) ---
def create_sponsorship_deposit(request, recipient_username):
    try:
        recipient = User.objects.select_related('wallet').get(username=recipient_username)
        recipient_wallet = recipient.wallet
    except (User.DoesNotExist, Wallet.DoesNotExist):
        messages.error(request, "The user you are trying to sponsor does not exist or does not have an active wallet.")
        return redirect('/')

    if request.method == 'POST':
        form = SponsorshipDepositForm(request.POST, user=request.user)
        if form.is_valid():
            with db_transaction.atomic():
                transaction = form.save(commit=False)
                transaction.wallet = recipient_wallet
                transaction.transaction_type = 'sponsorship_deposit'
                transaction.status = 'awaiting_admin_instructions'

                if request.user.is_authenticated:
                    transaction.sponsor = request.user
                    desc = f"Sponsorship from {request.user.username}. "
                else:
                    desc = f"Guest sponsorship from {form.cleaned_data.get('sponsor_guest_name') or form.cleaned_data.get('sponsor_guest_email')}. "

                if form.cleaned_data.get('description'):
                    desc += f"Message: '{form.cleaned_data.get('description')}'"

                transaction.description = desc
                transaction.save()

                messages.success(request, f"Thank you for sponsoring {recipient.username}! Your request has been submitted. An admin will provide payment instructions soon.")
                return redirect('/')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SponsorshipDepositForm(user=request.user)

    context = {
        'form': form,
        'recipient': recipient,
    }
    return render(request, 'wallet/sponsorship_form.html', context)


# --- ALL OTHER VIEWS (Unchanged) ---
# The rest of your views.py file remains the same.
# The nowpayments_ipn view is generic and will handle the new sponsorship type automatically.

def get_min_amount(crypto_code):
    url = f"{NOWPAYMENTS_BASE_URL}/min-amount"
    headers = {"x-api-key": NOWPAYMENTS_API_KEY}
    params = {"currency_from": "usd", "currency_to": crypto_code}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return Decimal(data.get('min_amount', '0'))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching minimum amount: {e}")
        return None

@login_required
def wallet_dashboard(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    all_transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')
    p2p_deposit_transactions = all_transactions.filter(transaction_type='deposit_p2p').exclude(status__in=['completed', 'failed', 'cancelled', 'refunded'])
    context = {'wallet': wallet, 'transactions': all_transactions, 'p2p_deposit_transactions': p2p_deposit_transactions}
    return render(request, 'wallet/wallet_dashboard.html', context)

@login_required
def crypto_deposit_request(request):
    if request.method == 'POST':
        form = CryptoDepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            crypto_currency_api_code = form.cleaned_data['crypto_currency']
            min_amount = get_min_amount(crypto_currency_api_code)
            if min_amount is not None and amount < min_amount:
                messages.error(request, f"The minimum deposit for {crypto_currency_api_code.upper()} is {min_amount} USD.")
                return render(request, 'wallet/crypto_deposit_request.html', {'form': form})
            wallet, _ = Wallet.objects.get_or_create(user=request.user)
            headers = {'x-api-key': NOWPAYMENTS_API_KEY, 'Content-Type': 'application/json'}
            payload = {
                "price_amount": str(amount), "price_currency": "usd", "pay_currency": crypto_currency_api_code,
                "ipn_callback_url": request.build_absolute_uri(reverse('wallet:nowpayments_ipn')),
                "order_id": f"deposit_{request.user.id}_{int(time.time())}",
                "success_url": request.build_absolute_uri(reverse('wallet:deposit_success_callback')),
                "cancel_url": request.build_absolute_uri(reverse('wallet:deposit_cancel_callback')),
            }
            try:
                response = requests.post(f"{NOWPAYMENTS_BASE_URL}/payment", headers=headers, json=payload)
                response.raise_for_status()
                nowpayments_data = response.json()
                if nowpayments_data.get('payment_id'):
                    Transaction.objects.create(wallet=wallet, transaction_type='deposit_crypto', amount=amount, status='pending', crypto_currency=crypto_currency_api_code, nowpayments_payment_id=nowpayments_data['payment_id'])
                    return render(request, 'wallet/crypto_deposit_details.html', {'nowpayments_data': nowpayments_data})
                else:
                    messages.error(request, "NOWPayments API error.")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Error connecting to NOWPayments: {e}")
    else:
        form = CryptoDepositForm()
    return render(request, 'wallet/crypto_deposit_request.html', {'form': form})

def donation_view(request):
    if request.method == 'POST':
        form = CryptoDepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            crypto_currency_api_code = form.cleaned_data['crypto_currency']
            wallet = request.user.wallet if request.user.is_authenticated else None
            user_id_for_order = str(request.user.id) if request.user.is_authenticated else str(uuid.uuid4())
            headers = {'x-api-key': NOWPAYMENTS_API_KEY, 'Content-Type': 'application/json'}
            payload = {
                "price_amount": str(amount), "price_currency": "usd", "pay_currency": crypto_currency_api_code,
                "ipn_callback_url": request.build_absolute_uri(reverse('wallet:nowpayments_ipn')),
                "order_id": f"donation_{user_id_for_order}_{int(time.time())}",
                "success_url": request.build_absolute_uri(reverse('wallet:deposit_success_callback')),
                "cancel_url": request.build_absolute_uri(reverse('wallet:deposit_cancel_callback')),
            }
            try:
                response = requests.post(f"{NOWPAYMENTS_BASE_URL}/payment", headers=headers, json=payload)
                response.raise_for_status()
                nowpayments_data = response.json()
                if nowpayments_data.get('payment_id'):
                    Transaction.objects.create(wallet=wallet, transaction_type='donation', amount=amount, status='pending', crypto_currency=crypto_currency_api_code, nowpayments_payment_id=nowpayments_data['payment_id'])
                    return render(request, 'wallet/crypto_deposit_details.html', {'nowpayments_data': nowpayments_data})
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Error connecting to NOWPayments: {e}")
    else:
        form = CryptoDepositForm()
    return render(request, 'wallet/donate.html', {'form': form})


@csrf_exempt
def nowpayments_ipn(request):
    """
    Handles IPN callbacks from NOWPayments for all transaction types.
    This view is now responsible for crediting user wallets AND emergency campaigns.
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    signature = request.headers.get('x-nowpayments-sig')
    request_body = request.body.decode('utf-8')
    if not signature or not verify_ipn_signature(request_body, signature, NOWPAYMENTS_IPN_SECRET):
        return HttpResponse("Invalid signature", status=403)

    try:
        payload_dict = json.loads(request_body)
        payment_id = payload_dict.get('payment_id')
        payment_status = payload_dict.get('payment_status')

        transaction = get_object_or_404(Transaction, nowpayments_payment_id=payment_id)

        if transaction.status == 'completed':
            return JsonResponse({'message': 'IPN already processed'}, status=200)

        if payment_status == 'finished':
            with db_transaction.atomic():
                # Lock the transaction row to prevent race conditions
                locked_transaction = Transaction.objects.select_for_update().get(pk=transaction.pk)
                if locked_transaction.status == 'completed':
                    return JsonResponse({'message': 'IPN already processed'}, status=200)

                # Mark transaction as complete
                locked_transaction.status = 'completed'
                locked_transaction.amount_received_crypto = Decimal(str(payload_dict.get('actually_paid', 0)))
                locked_transaction.tx_hash = payload_dict.get('payin_hash')

                # --- NEW LOGIC: Check transaction type and act accordingly ---
                if locked_transaction.transaction_type == 'emergency_donation_crypto':
                    campaign = locked_transaction.campaign
                    if campaign:
                        # Use select_for_update to lock the campaign row
                        locked_campaign = campaign.__class__.objects.select_for_update().get(pk=campaign.pk)
                        # We use the original USD amount for the campaign goal
                        locked_campaign.current_amount += locked_transaction.amount
                        locked_campaign.save()

                # Original logic: Credit a user's wallet
                elif locked_transaction.wallet:
                    locked_wallet = Wallet.objects.select_for_update().get(pk=locked_transaction.wallet.pk)
                    # We use the original USD amount for the wallet deposit
                    locked_wallet.update_balance(locked_transaction.amount, is_credit=True)
                
                locked_transaction.save()

        elif payment_status in ['failed', 'refunded', 'expired']:
            if transaction.status != 'completed':
                transaction.status = payment_status
                transaction.save()

        return JsonResponse({'message': 'IPN processed successfully'}, status=200)

    except (json.JSONDecodeError, Transaction.DoesNotExist):
        return HttpResponse("Invalid request or transaction not found", status=400)
    except Exception:
        # Generic catch for other potential errors
        return HttpResponse("Internal server error", status=500)


def verify_ipn_signature(request_body: str, signature: str, secret_key: str) -> bool:
    if not secret_key: return False
    try:
        # Use dumps with separators to ensure no whitespace, matching NOWPayments' format
        sorted_payload_str = json.dumps(json.loads(request_body), sort_keys=True, separators=(',', ':'))
        calculated_signature = hmac.new(secret_key.encode('utf-8'), msg=sorted_payload_str.encode('utf-8'), digestmod=hashlib.sha512).hexdigest()
        return hmac.compare_digest(calculated_signature, signature)
    except Exception:
        return False

@login_required
def deposit_success_callback(request):
    messages.success(request, "Your payment process was successful. The recipient's wallet will be updated shortly.")
    return redirect('wallet:wallet_dashboard')

@login_required
def deposit_cancel_callback(request):
    messages.error(request, "Your payment process was cancelled.")
    return redirect('wallet:wallet_dashboard')

@csrf_exempt
def get_minimum_amount_api(request):
    crypto_code = request.GET.get('crypto')
    if crypto_code:
        min_amount = get_min_amount(crypto_code)
        return JsonResponse({'min_amount': str(min_amount)})
    return JsonResponse({'error': 'No crypto provided'}, status=400)

@login_required
def p2p_deposit_request(request):
    if request.method == 'POST':
        form = P2PDepositRequestForm(request.POST)
        if form.is_valid():
            with db_transaction.atomic():
                transaction = form.save(commit=False)
                transaction.wallet = request.user.wallet
                transaction.transaction_type = 'deposit_p2p'
                transaction.status = 'awaiting_admin_instructions'
                transaction.save()
                messages.info(request, "Your P2P deposit request has been submitted.")
                return redirect('wallet:wallet_dashboard')
    else:
        form = P2PDepositRequestForm()
    return render(request, 'wallet/p2p_deposit_request.html', {'form': form})

@login_required
def p2p_deposit_upload_proof(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id, wallet__user=request.user)
    if transaction.status != 'awaiting_proof_of_payment':
        messages.error(request, "Proof of payment cannot be uploaded for this transaction.")
        return redirect('wallet:wallet_dashboard')
    if request.method == 'POST':
        form = ProofOfPaymentUploadForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            with db_transaction.atomic():
                form.save()
                transaction.status = 'review'
                transaction.save()
                messages.success(request, "Proof of payment uploaded successfully.")
                return redirect('wallet:wallet_dashboard')
    else:
        form = ProofOfPaymentUploadForm(instance=transaction)
    return render(request, 'wallet/p2p_deposit_upload_proof.html', {'form': form, 'transaction': transaction})

@login_required
def internal_transfer(request):
    if request.method == 'POST':
        form = InternalTransferForm(request.POST, user=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient_username']
            amount = form.cleaned_data['amount']
            with db_transaction.atomic():
                sender_wallet = request.user.wallet
                recipient_wallet = recipient.wallet
                sender_wallet.update_balance(amount, is_credit=False)
                Transaction.objects.create(wallet=sender_wallet, transaction_type='internal_transfer_send', amount=amount, status='completed', receiver_wallet=recipient_wallet)
                recipient_wallet.update_balance(amount, is_credit=True)
                Transaction.objects.create(wallet=recipient_wallet, transaction_type='internal_transfer_receive', amount=amount, status='completed', sender_wallet=sender_wallet)
                messages.success(request, f"Successfully transferred {amount} to {recipient.username}.")
                return redirect('wallet:wallet_dashboard')
    else:
        form = InternalTransferForm(user=request.user)
    return render(request, 'wallet/internal_transfer.html', {'form': form})

@login_required
def crypto_withdrawal_request(request):
    wallet = request.user.wallet
    if request.method == 'POST':
        form = CryptoWithdrawalForm(request.POST, user=request.user)
        if form.is_valid():
            with db_transaction.atomic():
                amount = form.cleaned_data['amount']
                wallet.update_balance(amount, is_credit=False)
                Transaction.objects.create(wallet=wallet, transaction_type='withdrawal_crypto', amount=amount, status='pending', crypto_currency=form.cleaned_data['crypto_currency'], crypto_address=form.cleaned_data['crypto_address'])
                messages.info(request, "Your crypto withdrawal request has been submitted.")
                return redirect('wallet:wallet_dashboard')
    else:
        form = CryptoWithdrawalForm(user=request.user)
    return render(request, 'wallet/crypto_withdrawal_request.html', {'form': form})

@login_required
def p2p_withdrawal_request(request):
    wallet = request.user.wallet
    if request.method == 'POST':
        form = P2PWithdrawalRequestForm(request.POST, user_wallet=wallet)
        if form.is_valid():
            with db_transaction.atomic():
                amount = form.cleaned_data['amount']
                wallet.update_balance(amount, is_credit=False)
                Transaction.objects.create(wallet=wallet, transaction_type='withdrawal_p2p', amount=amount, status='pending', payment_method=form.cleaned_data['payment_method'], payment_details=form.cleaned_data['payment_details'])
                messages.info(request, "Your P2P withdrawal request has been submitted.")
                return redirect('wallet:wallet_dashboard')
    else:
        form = P2PWithdrawalRequestForm(user_wallet=wallet)
    return render(request, 'wallet/p2p_withdrawal_request.html', {'form': form})
