import hmac
import hashlib
import json
import requests
from decimal import Decimal
import logging
import qrcode
from io import BytesIO
import base64
import uuid # Needed for uuid.uuid4()

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db import transaction as db_transaction
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone # Added for timezone.now()

from .models import Wallet, Transaction
from .forms import (
    InternalTransferForm, CryptoDepositForm, P2PDepositRequestForm, P2PDepositUploadProofForm,
    CryptoWithdrawalForm, P2PWithdrawalRequestForm, CryptoDonationForm
)

logger = logging.getLogger(__name__)

# Helper to get or create wallet
def get_user_wallet(user):
    wallet, created = Wallet.objects.get_or_create(owner=user)
    if created:
        messages.info(None, "Your wallet has been created.")
    return wallet

@login_required
def wallet_dashboard(request):
    wallet = get_user_wallet(request.user)
    # Get pending P2P deposit requests for the current user
    p2p_deposit_transactions = Transaction.objects.filter(
        wallet=wallet,
        transaction_type='p2p_deposit'
    ).exclude(status__in=['completed', 'failed', 'cancelled']).order_by('-timestamp')

    transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')[:10] # Last 10 transactions

    context = {
        'wallet': wallet,
        'p2p_deposit_transactions': p2p_deposit_transactions,
        'transactions': transactions,
    }
    return render(request, 'wallet/wallet_dashboard.html', context)

@login_required
def deposit_method_selection(request):
    return render(request, 'wallet/deposit_method_selection.html')

@login_required
def withdrawal_method_selection(request):
    """
    Renders a page for the user to select their withdrawal method (Crypto or P2P).
    """
    return render(request, 'wallet/withdrawal_method_selection.html')

@login_required
def internal_transfer(request):
    wallet = get_user_wallet(request.user)
    if request.method == 'POST':
        # Pass the wallet instance so the form can perform balance checks
        form = InternalTransferForm(request.POST, sender_wallet=wallet)
        if form.is_valid():
            # recipient_user is attached to the form instance in clean_recipient_username
            recipient_user = form.recipient_user 
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', '')

            with db_transaction.atomic():
                # Get or create recipient's wallet
                recipient_wallet = get_user_wallet(recipient_user)

                # Sender's wallet withdrawal
                wallet.withdraw(
                    amount=amount,
                    transaction_type='internal_transfer_send',
                    description=f"Transfer to {recipient_user.username}: {description}",
                    receiver_wallet=recipient_wallet # Pass receiver wallet to the transaction
                )

                # Recipient's wallet deposit
                recipient_wallet.deposit(
                    amount=amount,
                    transaction_type='internal_transfer_receive',
                    description=f"Transfer from {request.user.username}: {description}",
                    sender_wallet=wallet # Pass sender wallet to the transaction
                )
                messages.success(request, f"Successfully transferred {amount} {wallet.currency} to {recipient_user.username}.")
                return redirect('wallet:wallet_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InternalTransferForm(sender_wallet=wallet)
    return render(request, 'wallet/internal_transfer.html', {'form': form, 'wallet': wallet})

@login_required
def crypto_deposit_request(request):
    wallet = get_user_wallet(request.user)
    # Define crypto choices for the form
    crypto_choices = [
        ('btc', 'Bitcoin (BTC)'),
        ('eth', 'Ethereum (ETH)'),
        ('usdttrc20', 'Tether (USDT on Tron/TRC20)'),
        ('usdtbep20', 'Tether (USDT on BSC/BEP20)'),
        ('ltc', 'Litecoin (LTC)'),
    ]

    if request.method == 'POST':
        # Pass crypto_choices to the form's __init__
        form = CryptoDepositForm(request.POST, crypto_choices=crypto_choices)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            crypto_currency = form.cleaned_data['crypto_currency']
            message = form.cleaned_data.get('message', '') # Get message from the form

            # NowPayments API call to create payment
            payload = {
                "price_amount": float(amount),
                "price_currency": wallet.currency.lower(), # Your base currency (e.g., usd)
                "pay_currency": crypto_currency.lower(),
                "ipn_callback_url": request.build_absolute_uri('/wallet/nowpayments_webhook/'),
                "order_id": str(wallet.owner.id) + "-" + str(uuid.uuid4()), # Unique order ID
                "order_description": f"Deposit to {request.user.username}'s wallet. Note: {message}",
                # "success_url": request.build_absolute_uri('/wallet/deposit_success/'), # Optional redirect
                # "cancel_url": request.build_absolute_uri('/wallet/deposit_cancel/'), # Optional redirect
            }
            headers = {
                'x-api-key': settings.NOWPAYMENTS_API_KEY,
                'Content-Type': 'application/json'
            }

            try:
                response = requests.post(settings.NOWPAYMENTS_API_URL + 'payment', headers=headers, json=payload)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                payment_data = response.json()
                logger.info(f"NowPayments API response: {payment_data}")

                if payment_data and 'payment_id' in payment_data:
                    # Create a pending transaction record
                    Transaction.objects.create(
                        wallet=wallet,
                        transaction_type='crypto_deposit',
                        amount=amount, # Amount in your base currency (e.g., USD)
                        status='pending', # Will be updated by IPN webhook
                        description=f"Crypto Deposit Request ({crypto_currency}). User note: {message}",
                        crypto_currency=crypto_currency,
                        nowpayments_payment_id=payment_data['payment_id'],
                        nowpayments_pay_address=payment_data.get('pay_address'),
                        nowpayments_pay_amount=Decimal(str(payment_data.get('pay_amount', '0.0'))), # Amount in crypto
                        nowpayments_order_id=payload['order_id']
                    )

                    # Generate QR code
                    qr_img_data = None
                    if payment_data.get('payment_url'): # NowPayments often provides a direct payment_url for QR
                        qr_data = payment_data['payment_url']
                    elif payment_data.get('pay_address') and payment_data.get('pay_amount'):
                        # Fallback to simple address and amount for QR
                        qr_data = f"{payment_data['pay_address']}?amount={payment_data.get('pay_amount')}"
                    else:
                        qr_data = payment_data.get('pay_address', 'No QR data available') # Should not happen

                    qr_img = qrcode.make(qr_data)
                    buffered_img = BytesIO()
                    qr_img.save(buffered_img, format="PNG")
                    qr_img_data = base64.b64encode(buffered_img.getvalue()).decode('utf-8')

                    messages.info(request, "Crypto deposit request initiated. Please send funds.")
                    return render(request, 'wallet/crypto_deposit_details.html', {
                        'payment_data': payment_data,
                        'qr_img_data': qr_img_data,
                        'wallet': wallet,
                    })
                else:
                    messages.error(request, "Failed to initiate crypto payment. No payment ID from NowPayments.")
            except requests.exceptions.RequestException as e:
                logger.error(f"NowPayments API request failed: {e}")
                messages.error(request, f"Error communicating with payment gateway: {e}. Check API key and URL.")
            except Exception as e:
                logger.error(f"An unexpected error occurred during crypto deposit request: {e}", exc_info=True)
                messages.error(request, "An unexpected error occurred. Please try again.")

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Pass crypto_choices to the form's __init__ for GET request
        form = CryptoDepositForm(crypto_choices=crypto_choices)
    return render(request, 'wallet/crypto_deposit_request.html', {'form': form, 'wallet': wallet})

@login_required
def crypto_deposit_details(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id, wallet__owner=request.user, transaction_type='crypto_deposit')
    qr_img_data = None
    
    # Reconstruct payment_data and QR data from the transaction object
    payment_data = {
        'pay_address': transaction.nowpayments_pay_address,
        'pay_amount': float(transaction.nowpayments_pay_amount) if transaction.nowpayments_pay_amount else 0.0,
        'payment_id': transaction.nowpayments_payment_id,
        'price_amount': float(transaction.amount),
        'price_currency': transaction.wallet.currency,
        'pay_currency': transaction.crypto_currency,
        # 'payment_url': transaction.nowpayments_payment_url # If you store this field
    }

    # Generate QR code
    qr_data = None
    # If you stored the original payment_url from NowPayments, use that. Otherwise, construct.
    # Assuming you don't store payment_url in Transaction model, using pay_address + pay_amount.
    if transaction.nowpayments_pay_address and transaction.nowpayments_pay_amount:
        qr_data = f"{transaction.nowpayments_pay_address}?amount={transaction.nowpayments_pay_amount}"

    if qr_data:
        qr_img = qrcode.make(qr_data)
        buffered_img = BytesIO()
        qr_img.save(buffered_img, format="PNG")
        qr_img_data = base64.b64encode(buffered_img.getvalue()).decode('utf-8')


    context = {
        'transaction': transaction,
        'payment_data': payment_data,
        'qr_img_data': qr_img_data
    }
    return render(request, 'wallet/crypto_deposit_details.html', context)


@csrf_exempt
def nowpayments_webhook(request):
    if request.method == 'POST':
        # Verify IPN signature
        try:
            signature = request.headers.get('X-NowPayments-Sig')
            if not signature:
                logger.error("NOWPayments Webhook: Missing X-NowPayments-Sig header.")
                return JsonResponse({'status': 'error', 'message': 'Missing signature'}, status=400)

            if not settings.NOWPAYMENTS_IPN_SECRET:
                logger.error("NOWPayments Webhook: NOWPAYMENTS_IPN_SECRET is not set.")
                return JsonResponse({'status': 'error', 'message': 'Webhook secret not configured'}, status=500)

            computed_signature = hmac.new(
                key=settings.NOWPAYMENTS_IPN_SECRET.encode(),
                msg=request.body, # Request body is already bytes
                digestmod=hashlib.sha512
            ).hexdigest() # Get the hex digest for comparison

            if not hmac.compare_digest(computed_signature, signature):
                logger.warning(f"NOWPayments Webhook: Invalid signature. Computed: {computed_signature}, Received: {signature}")
                return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=403)

            # Parse the payload
            payload = json.loads(request.body.decode('utf-8'))
            payment_id = payload.get('payment_id')
            payment_status = payload.get('payment_status')
            pay_amount = Decimal(str(payload.get('pay_amount', '0.0'))) # Amount user paid in crypto
            price_amount = Decimal(str(payload.get('price_amount', '0.0'))) # Amount in fiat (USD)
            price_currency = payload.get('price_currency')
            order_id = payload.get('order_id') # Your internal order ID

            logger.info(f"NOWPayments Webhook received: Payment ID {payment_id}, Status {payment_status}")

            try:
                # Find the corresponding transaction
                transaction = Transaction.objects.get(nowpayments_payment_id=payment_id)
                wallet = transaction.wallet

                # Update transaction status and wallet balance based on payment_status
                if payment_status == 'finished':
                    if transaction.status != 'completed': # Prevent double-spending
                        with db_transaction.atomic():
                            wallet.balance += price_amount # Add amount in base currency (USD)
                            wallet.save(update_fields=['balance'])
                            transaction.status = 'completed'
                            transaction.description = f"Crypto Deposit {transaction.crypto_currency} (Finished) - {transaction.nowpayments_payment_id}"
                            transaction.timestamp = timezone.now() # Update timestamp to completion time
                            transaction.amount = price_amount # Ensure the stored amount is the USD value received
                            transaction.save(update_fields=['status', 'amount', 'description', 'timestamp'])
                        logger.info(f"NOWPayments Webhook: Payment {payment_id} finished. Wallet {wallet.owner.username} credited {price_amount} {price_currency}.")
                        # messages.success(request, f"Your crypto deposit of {price_amount} {price_currency} has been completed.") # Webhooks don't send messages to user directly
                    else:
                        logger.info(f"NOWPayments Webhook: Payment {payment_id} already completed. No action taken.")
                elif payment_status in ['failed', 'refunded', 'expired', 'partially_paid', 'cancelled']: # Include cancelled for completeness
                    if transaction.status not in ['failed', 'cancelled', 'refunded', 'expired']: # Prevent redundant updates
                        transaction.status = payment_status
                        transaction.description = f"Crypto Deposit {transaction.crypto_currency} ({payment_status}) - {transaction.nowpayments_payment_id}"
                        transaction.timestamp = timezone.now()
                        transaction.save(update_fields=['status', 'description', 'timestamp'])
                    logger.warning(f"NOWPayments Webhook: Payment {payment_id} status changed to {payment_status}. No balance update.")
                else:
                    # For 'waiting', 'confirming', 'sending' etc. - just update status
                    if transaction.status != payment_status: # Avoid unnecessary saves
                        transaction.status = payment_status
                        transaction.save(update_fields=['status'])
                    logger.info(f"NOWPayments Webhook: Payment {payment_id} status updated to {payment_status}.")

            except Transaction.DoesNotExist:
                logger.error(f"NOWPayments Webhook: Transaction with payment_id {payment_id} not found.")
                return JsonResponse({'status': 'error', 'message': 'Transaction not found'}, status=404)
            except Exception as e:
                logger.error(f"NOWPayments Webhook processing error: {e}", exc_info=True)
                return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

            return JsonResponse({'status': 'ok'})

        except json.JSONDecodeError:
            logger.error("NOWPayments Webhook: Invalid JSON payload.")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"NOWPayments Webhook general error: {e}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def p2p_deposit_request(request):
    wallet = get_user_wallet(request.user)
    if request.method == 'POST':
        form = P2PDepositRequestForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            payment_details = form.cleaned_data['payment_details'] 
            description = form.cleaned_data.get('description', '')

            try:
                # Create the P2P deposit request transaction
                # The deposit method handles saving the transaction and setting initial status
                transaction = wallet.deposit(
                    amount=amount,
                    transaction_type='p2p_deposit',
                    payment_method=payment_method,
                    payment_details=payment_details,
                    description=f"P2P Deposit Request via {payment_method}: {description}",
                    status='awaiting_admin_instructions' # Explicitly set initial status
                )
                messages.success(request, f"Your P2P deposit request for {amount} {wallet.currency} has been submitted. Please await admin instructions on the transaction details page.")
                return redirect('wallet:p2p_deposit_details', transaction_id=transaction.transaction_id) # Redirect to details
            except Exception as e:
                logger.error(f"Error submitting P2P deposit request: {e}", exc_info=True)
                messages.error(request, "There was an error processing your request. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = P2PDepositRequestForm()
    return render(request, 'wallet/p2p_deposit_request.html', {'form': form, 'wallet': wallet})

@login_required
def p2p_deposit_upload_proof(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        transaction_id=transaction_id,
        wallet__owner=request.user,
        transaction_type='p2p_deposit',
        status__in=['awaiting_proof_of_payment', 'in_review'] # Allow re-upload if needed
    )

    if request.method == 'POST':
        form = P2PDepositUploadProofForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            # The form handles saving the file to the instance automatically
            form.save(commit=False) # Save the file to the model instance but don't commit yet

            # Update status and description
            transaction.status = 'in_review' # Status changes to in_review after proof upload
            transaction.description = f"P2P Deposit: Proof Uploaded for {transaction.amount} {transaction.wallet.currency}. Awaiting Admin Review."
            transaction.save(update_fields=['user_proof_of_payment', 'status', 'description'])

            messages.success(request, "Proof of payment uploaded successfully. Awaiting admin verification.")
            return redirect('wallet:p2p_deposit_details', transaction_id=transaction.transaction_id) # Redirect back to details page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = P2PDepositUploadProofForm(instance=transaction)

    context = {
        'form': form,
        'transaction': transaction,
        'wallet': get_user_wallet(request.user)
    }
    return render(request, 'wallet/p2p_deposit_upload_proof.html', context)

@login_required
def p2p_deposit_details(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        transaction_id=transaction_id,
        wallet__owner=request.user,
        transaction_type='p2p_deposit'
    )
    context = {
        'transaction': transaction,
        'wallet': get_user_wallet(request.user)
    }
    return render(request, 'wallet/p2p_deposit_details.html', context)


@login_required
def crypto_withdrawal_request(request):
    wallet = get_user_wallet(request.user)
    # Define a minimum withdrawal amount for crypto, this can come from settings
    min_withdrawal = Decimal('10.00') # Example minimum

    if request.method == 'POST':
        form = CryptoWithdrawalForm(request.POST, user_wallet=wallet, min_withdrawal_amount=min_withdrawal)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            crypto_currency = form.cleaned_data['crypto_currency']
            crypto_address = form.cleaned_data['crypto_address']
            description = form.cleaned_data.get('description', '')

            try:
                # Withdrawal automatically sets status to 'pending' and deducts balance
                transaction = wallet.withdraw(
                    amount=amount,
                    transaction_type='withdrawal_crypto',
                    description=f"Crypto Withdrawal ({crypto_currency}) to {crypto_address}: {description}",
                    crypto_currency=crypto_currency,
                    crypto_address=crypto_address
                )
                messages.success(request, f"Your crypto withdrawal request for {amount} {wallet.currency} to {crypto_currency} has been submitted and is pending admin approval.")
                return redirect('wallet:wallet_dashboard')
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                logger.error(f"Error submitting crypto withdrawal request: {e}", exc_info=True)
                messages.error(request, "There was an error processing your request. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CryptoWithdrawalForm(user_wallet=wallet, min_withdrawal_amount=min_withdrawal)
    return render(request, 'wallet/crypto_withdrawal_request.html', {'form': form, 'wallet': wallet})

@login_required
def p2p_withdrawal_request(request):
    wallet = get_user_wallet(request.user)
    # Define a minimum withdrawal amount for P2P, this can come from settings
    min_withdrawal = Decimal('5.00') # Example minimum

    if request.method == 'POST':
        form = P2PWithdrawalRequestForm(request.POST, user_wallet=wallet, min_withdrawal_amount=min_withdrawal)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            # Correctly retrieve the field name from the form (now recipient_account_details)
            recipient_account_details = form.cleaned_data['recipient_account_details'] 
            description = form.cleaned_data.get('description', '')

            try:
                # Withdrawal automatically sets status to 'pending' and deducts balance
                transaction = wallet.withdraw(
                    amount=amount,
                    transaction_type='withdrawal_p2p',
                    description=f"P2P Withdrawal via {payment_method}: {description}",
                    payment_method=payment_method,
                    recipient_account_details=recipient_account_details # Pass correct field name
                )
                messages.success(request, f"Your P2P withdrawal request for {amount} {wallet.currency} has been submitted and is pending admin approval.")
                return redirect('wallet:wallet_dashboard')
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                logger.error(f"Error submitting P2P withdrawal request: {e}", exc_info=True)
                messages.error(request, "There was an error processing your request. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = P2PWithdrawalRequestForm(user_wallet=wallet, min_withdrawal_amount=min_withdrawal)
    return render(request, 'wallet/p2p_withdrawal_request.html', {'form': form, 'wallet': wallet})

@login_required
def donate(request):
    wallet = get_user_wallet(request.user)
    # Define crypto choices for the form
    crypto_choices = [
        ('btc', 'Bitcoin (BTC)'),
        ('eth', 'Ethereum (ETH)'),
        ('usdttrc20', 'Tether (USDT on Tron/TRC20)'),
        ('usdtbep20', 'Tether (USDT on BSC/BEP20)'),
        ('ltc', 'Litecoin (LTC)'),
    ]
    # Define a minimum donation amount
    min_donation = Decimal('1.00') # Assuming minimum for USD equivalent

    if request.method == 'POST':
        # Pass user_wallet and crypto_choices to the CryptoDonationForm
        form = CryptoDonationForm(request.POST, user_wallet=wallet, crypto_choices=crypto_choices)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            crypto_currency = form.cleaned_data['crypto_currency'] 
            user_message = form.cleaned_data.get('message', '') # 'message' from CryptoDepositForm
            donor_name = form.cleaned_data.get('donor_name', 'Anonymous')

            # Ensure DONATION_CRYPTO_ADDRESS is set in settings.py if actually sending out
            donation_address = getattr(settings, 'DONATION_CRYPTO_ADDRESS', None)
            if not donation_address:
                messages.error(request, "Donation address not configured. Please contact support.")
                logger.error("DONATION_CRYPTO_ADDRESS is not set in settings.py for donation view.")
                # Re-render the form with errors or redirect back
                return render(request, 'wallet/donate.html', {'form': form, 'wallet': wallet})


            try:
                # The 'donate' view here uses wallet.withdraw as it reduces the user's balance.
                transaction = wallet.withdraw(
                    amount=amount,
                    transaction_type='donation',
                    description=f"Donation from {donor_name} ({crypto_currency}). Note: {user_message}",
                    crypto_currency=crypto_currency,
                    crypto_address=donation_address, # The predefined donation address
                    status='pending' # Donations are likely pending admin/system processing
                )
                messages.success(request, f"Your donation of {amount} {wallet.currency} has been submitted. Thank you!")
                return redirect('wallet:wallet_dashboard') # Or a donation success page
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                logger.error(f"Error processing donation: {e}", exc_info=True)
                messages.error(request, "There was an error processing your donation. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # For GET request, instantiate with user_wallet and crypto_choices
        form = CryptoDonationForm(user_wallet=wallet, crypto_choices=crypto_choices)
    return render(request, 'wallet/donate.html', {'form': form, 'wallet': wallet})

@login_required
def crypto_donation_details(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id, wallet__owner=request.user, transaction_type='donation')
    context = {
        'transaction': transaction,
        'wallet': get_user_wallet(request.user)
    }
    return render(request, 'wallet/crypto_donation_details.html', context)


# Admin-related views remain commented out as they are best handled via Django Admin.
# ... (admin views as per your original file)
