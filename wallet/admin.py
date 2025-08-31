# wallet/admin.py (UPDATED TO MANAGE ALL SPONSORSHIP TYPES)
from django.utils import timezone
from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction as db_transaction
from django.utils.html import format_html
from django import forms
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType # Import ContentType

from .models import Wallet, Transaction

User = get_user_model()

# --- Custom Form for Manual Wallet Adjustments ---
class CreditDebitForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    amount = forms.DecimalField(max_digits=18, decimal_places=8, min_value=Decimal('0.00000001'), label="Amount")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description/Notes")
    is_credit = forms.BooleanField(required=False, initial=True, label="Is Credit (Deposit)")

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at', 'updated_at', 'admin_actions_column')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('credit-debit/', self.admin_site.admin_view(self.credit_debit_view), name='wallet_wallet_credit_debit'),
        ]
        return custom_urls + urls

    def admin_actions_column(self, obj):
        credit_url = reverse('admin:wallet_wallet_credit_debit') + f"?user_id={obj.user.pk}&action=credit"
        debit_url = reverse('admin:wallet_wallet_credit_debit') + f"?user_id={obj.user.pk}&action=debit"
        return format_html(
            f'<a class="button" href="{credit_url}">Credit</a> '
            f'<a class="button" href="{debit_url}">Debit</a>'
        )
    admin_actions_column.short_description = 'Admin Actions'

    def credit_debit_view(self, request):
        form = CreditDebitForm()
        if request.method == 'POST':
            form = CreditDebitForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                amount = form.cleaned_data['amount']
                description = form.cleaned_data['description']
                is_credit = form.cleaned_data['is_credit']
                try:
                    with db_transaction.atomic():
                        wallet = Wallet.objects.get(user=user)
                        wallet.update_balance(amount, is_credit=is_credit)
                        transaction_type = 'manual_credit' if is_credit else 'manual_debit'
                        Transaction.objects.create(
                            wallet=wallet,
                            transaction_type=transaction_type,
                            amount=amount,
                            status='completed',
                            description=f"Admin action: {description}",
                            admin_notes=f"Admin {request.user.username} performed a manual action on {timezone.now()}."
                        )
                    messages.success(request, f"Wallet for {user.username} updated.")
                    return redirect(reverse('admin:wallet_wallet_changelist'))
                except Wallet.DoesNotExist:
                    messages.error(request, f"Wallet for {user.username} not found.")
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")
        context = self.admin_site.each_context(request)
        context.update({'title': "Credit/Debit Wallet", 'form': form})
        return render(request, 'admin/wallet/credit_debit_form.html', context)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'transaction_type',
        'recipient_user',
        'sponsor_info',
        'amount',
        'status',
        'timestamp',
        'admin_actions_column'
    )
    list_filter = ('transaction_type', 'status', 'timestamp')
    search_fields = (
        'wallet__user__username', # Search by recipient
        'sponsor__username',      # Search by logged-in sponsor
        'sponsor_guest_email',    # Search by guest sponsor email
        'transaction_id',
        'description',
        'nowpayments_payment_id',
    )
    readonly_fields = (
        'timestamp', 'transaction_id', 'nowpayments_payment_id',
        'tx_hash', 'sender_wallet', 'receiver_wallet',
        'sponsor', 'sponsor_guest_email', 'sponsor_guest_name'
    )
    fieldsets = (
        ('Primary Details', {
            'fields': ('wallet', 'transaction_type', 'amount', 'fee', 'description')
        }),
        ('Status & Management', {
            'fields': ('status', 'admin_notes', 'admin_payment_instructions', 'user_proof_of_payment'),
        }),
        ('Sponsor Information (if applicable)', {
            'fields': ('sponsor', 'sponsor_guest_name', 'sponsor_guest_email'),
            'classes': ('collapse',),
        }),
        ('Crypto Details (if applicable)', {
            'fields': ('nowpayments_payment_id', 'crypto_currency', 'crypto_address', 'tx_hash', 'amount_received_crypto'),
            'classes': ('collapse',),
        }),
        ('P2P Details (if applicable)', {
            'fields': ('payment_method', 'payment_details'),
            'classes': ('collapse',),
        }),
        ('Internal Transfer Details (if applicable)', {
            'fields': ('sender_wallet', 'receiver_wallet'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('timestamp', 'transaction_id'),
            'classes': ('collapse', 'wide'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('wallet__user', 'sponsor')

    def recipient_user(self, obj):
        if obj.wallet and obj.wallet.user:
            return obj.wallet.user.username
        return "N/A (Anonymous Donation)"
    recipient_user.short_description = 'Recipient User'
    recipient_user.admin_order_field = 'wallet__user__username'

    def sponsor_info(self, obj):
        # Handle both manual and crypto sponsorships
        if obj.transaction_type in ['sponsorship_deposit', 'sponsorship_crypto']:
            if obj.sponsor:
                try:
                    ct = ContentType.objects.get_for_model(obj.sponsor)
                    sponsor_url = reverse(f'admin:{ct.app_label}_{ct.model}_change', args=[obj.sponsor.pk])
                    return format_html('<a href="{}">{} (User)</a>', sponsor_url, obj.sponsor.username)
                except Exception: # Catching generic Exception for robustness in admin display
                    # fallback if reverse fails, just display username
                    return f"{obj.sponsor.username} (User)"
            elif obj.sponsor_guest_email:
                name = obj.sponsor_guest_name or 'Guest'
                return f"{name} ({obj.sponsor_guest_email})"
        return "N/A"
    sponsor_info.short_description = 'Sponsor'

    def display_user_proof(self, obj):
        if obj.user_proof_of_payment:
            return format_html(f'<a href="{obj.user_proof_of_payment.url}" target="_blank">View Proof</a>')
        return "N/A"
    display_user_proof.short_description = 'Proof of Payment'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/approve/', self.admin_site.admin_view(self.approve_transaction), name='wallet_transaction_approve'),
            path('<path:object_id>/reject/', self.admin_site.admin_view(self.reject_transaction), name='wallet_transaction_reject'),
            path('<path:object_id>/provide-instructions/', self.admin_site.admin_view(self.provide_p2p_instructions_view), name='wallet_transaction_provide_instructions'),
        ]
        return custom_urls + urls

    def admin_actions_column(self, obj):
        actions = []
        # Logic for showing buttons only for manual transaction types that require admin intervention.
        # sponsorship_crypto is automated and does not need these buttons.
        if obj.transaction_type in ['deposit_p2p', 'sponsorship_deposit']:
            if obj.status == 'awaiting_admin_instructions':
                url = reverse('admin:wallet_transaction_provide_instructions', args=[obj.pk])
                actions.append(f'<a class="button" href="{url}">Provide Instructions</a>')
            elif obj.status == 'review' and obj.user_proof_of_payment:
                approve_url = reverse('admin:wallet_transaction_approve', args=[obj.pk])
                reject_url = reverse('admin:wallet_transaction_reject', args=[obj.pk])
                actions.append(f'<a class="button" href="{approve_url}">Approve</a>')
                actions.append(f'<a class="button" href="{reject_url}">Reject</a>')
       
        elif obj.transaction_type in ['withdrawal_crypto', 'withdrawal_p2p'] and obj.status == 'pending':
            approve_url = reverse('admin:wallet_transaction_approve', args=[obj.pk])
            reject_url = reverse('admin:wallet_transaction_reject', args=[obj.pk])
            actions.append(f'<a class="button" href="{approve_url}">Approve</a>')
            actions.append(f'<a class="button" href="{reject_url}">Reject</a>')

        if not actions:
            return "N/A"
        return format_html(' '.join(actions))
    admin_actions_column.short_description = 'Admin Actions'

    def provide_p2p_instructions_view(self, request, object_id):
        # This view remains unchanged
        transaction = get_object_or_404(Transaction, pk=object_id)
        if request.method == 'POST':
            instructions = request.POST.get('instructions')
            if instructions:
                transaction.admin_payment_instructions = instructions
                transaction.status = 'awaiting_proof_of_payment'
                transaction.save()
                messages.success(request, "Instructions provided and transaction status updated.")
                return redirect(reverse('admin:wallet_transaction_changelist'))
            else:
                messages.error(request, "Instructions cannot be empty.")
        context = self.admin_site.each_context(request)
        context.update({'transaction': transaction, 'title': f"Provide Instructions for {transaction.transaction_id}"})
        return render(request, 'admin/wallet/transaction/provide_instructions_form.html', context)

    def approve_transaction(self, request, object_id):
        transaction = get_object_or_404(Transaction, pk=object_id)
        with db_transaction.atomic():
            # This logic correctly handles crediting the wallet for manual deposits and sponsorships.
            # It correctly IGNORES automated crypto transactions, which are handled by the IPN.
            if transaction.transaction_type in ['deposit_p2p', 'sponsorship_deposit']:
                wallet = transaction.wallet
                if wallet:
                    wallet.update_balance(transaction.amount, is_credit=True)
                    transaction.status = 'completed'
                    transaction.admin_notes = f"Approved by {request.user.username} on {timezone.now()}."
                    transaction.save()
                    messages.success(request, f"Transaction {transaction.transaction_id} approved and wallet credited.")
                else:
                    messages.error(request, f"Cannot approve transaction {transaction.transaction_id}: Wallet not found.")
            
            # This logic handles debiting the wallet for withdrawals
            elif transaction.transaction_type in ['withdrawal_crypto', 'withdrawal_p2p']:
                transaction.status = 'completed'
                transaction.admin_notes = f"Withdrawal approved by {request.user.username} on {timezone.now()}."
                transaction.save()
                messages.success(request, f"Withdrawal {transaction.transaction_id} approved.")

        return redirect(reverse('admin:wallet_transaction_changelist'))

    def reject_transaction(self, request, object_id):
        transaction = get_object_or_404(Transaction, pk=object_id)
        with db_transaction.atomic():
            # For withdrawals, we need to refund the balance to the user's wallet
            if transaction.transaction_type in ['withdrawal_crypto', 'withdrawal_p2p']:
                wallet = transaction.wallet
                if wallet:
                    wallet.update_balance(transaction.amount, is_credit=True) # Refund the amount
                    messages.info(request, f"Amount of {transaction.amount} refunded to {wallet.user.username}'s wallet.")
            
            transaction.status = 'failed' # Or 'rejected' if you add that status
            transaction.admin_notes = f"Rejected by {request.user.username} on {timezone.now()}."
            transaction.save()
            messages.warning(request, f"Transaction {transaction.transaction_id} has been rejected.")
        return redirect(reverse('admin:wallet_transaction_changelist'))

    # --- Permissions ---
    def has_add_permission(self, request):
        # Generally, transactions should be created by users, not admins directly.
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        # Deleting transactions can be risky for auditing.
        # Only allow superusers to do this.
        return request.user.is_superuser
