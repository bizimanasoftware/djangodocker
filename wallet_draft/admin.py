# wallet/admin.py
from django.contrib import admin, messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Wallet, Transaction
from .forms import AdminInstructionForm, AdminCompletionForm

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    # CORRECTED: Changed 'user' to 'owner' to match the Wallet model field
    list_display = ('owner', 'balance', 'updated_at')
    # CORRECTED: Changed 'user__username' to 'owner__username'
    search_fields = ('owner__username',)
    # CORRECTED: Changed 'user' to 'owner'
    readonly_fields = ('owner', 'balance', 'created_at', 'updated_at')
    list_per_page = 25

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'amount', 'status', 'timestamp', 'transaction_type')
    list_filter = ('status', 'transaction_type', 'crypto_currency')
    # CORRECTED: Changed 'user__username' to 'wallet__owner__username'
    # Explanation: Transaction links to Wallet (via 'wallet' field),
    # and Wallet links to User (via 'owner' field), so it's wallet__owner__username
    search_fields = ('wallet__owner__username', 'transaction_id__hex', 'txid', 'crypto_address', 'nowpayments_payment_id')
    readonly_fields = [f.name for f in Transaction._meta.fields if f.name not in [
        'status', 'admin_notes', 'admin_payment_instructions', 'txid'
    ]] # Make most fields read-only for safety
    list_per_page = 30
    actions = [
        'provide_payment_instructions',
        'confirm_p2p_payment',
        'mark_withdrawal_completed',
        'fail_and_refund_withdrawal'
    ]

    def get_readonly_fields(self, request, obj=None):
        # Allow editing certain fields only for specific transaction types/statuses
        if obj:
            # Note: Changed 'deposit_p2p' to 'p2p_deposit' to match your TRANSACTION_TYPES tuple in models.py
            if obj.transaction_type == 'p2p_deposit' and obj.status == 'awaiting_admin_instructions':
                return [f.name for f in Transaction._meta.fields if f.name not in ['admin_payment_instructions', 'status']]
        return self.readonly_fields

    @admin.action(description='P2P: Provide Payment Instructions')
    def provide_payment_instructions(self, request, queryset):
        # Action for P2P deposits awaiting instructions
        # Note: Changed 'deposit_p2p' to 'p2p_deposit'
        queryset = queryset.filter(transaction_type='p2p_deposit', status='awaiting_admin_instructions')
        if 'apply' in request.POST:
            form = AdminInstructionForm(request.POST)
            if form.is_valid():
                instructions = form.cleaned_data['instructions']
                updated_count = queryset.update(
                    admin_payment_instructions=instructions,
                    status='awaiting_proof_of_payment'
                )
                self.message_user(request, f"{updated_count} transactions updated to 'Awaiting Proof of Payment'.", messages.SUCCESS)
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = AdminInstructionForm()

        return render(request, 'admin/actions/admin_instruction.html', {'items': queryset, 'form': form})

    @admin.action(description='P2P: Confirm & Complete Payment')
    def confirm_p2p_payment(self, request, queryset):
        # Action for P2P deposits under review
        # Note: Changed 'deposit_p2p' to 'p2p_deposit'
        queryset = queryset.filter(transaction_type='p2p_deposit', status='in_review') # Corrected 'review' to 'in_review' to match TRANSACTION_STATUSES
        updated_count = 0
        for transaction in queryset:
            try:
                # Accessing wallet via transaction.wallet, then owner, then wallet again.
                # The deposit method is on the Wallet instance itself.
                # So, it should be transaction.wallet.deposit(...)
                # And ensure you're passing all required arguments if it's called this way.
                # If transaction.user.wallet was working previously, it implies
                # that your Transaction model might implicitly create a 'user' attribute
                # if there's a related_name somewhere, but `wallet.owner` is more explicit.
                # Let's use the explicit `wallet.owner.wallet` if it's a direct reference back.
                # However, the `deposit` method is on `Wallet` object, `transaction.wallet` is already the Wallet object.
                # Corrected to use transaction.wallet directly.
                transaction.wallet.deposit(
                    amount=transaction.amount,
                    transaction_type=transaction.transaction_type, # Keep original type
                    # You might need to pass other relevant fields from the transaction
                    # to the deposit method, depending on how specific your deposit logic is.
                    # For a simple "complete" action, just amount might be enough for balance update.
                )
                transaction.status = 'completed'
                transaction.save()
                updated_count += 1
            except Exception as e:
                self.message_user(request, f"Error processing {transaction.transaction_id}: {e}", messages.ERROR)
        if updated_count > 0:
            self.message_user(request, f"{updated_count} P2P deposits were confirmed and completed.", messages.SUCCESS)

    @admin.action(description='Withdrawal: Mark as Processed & Complete')
    def mark_withdrawal_completed(self, request, queryset):
        # Action for pending withdrawals
        queryset = queryset.filter(transaction_type__in=['withdrawal_crypto', 'withdrawal_p2p'], status='pending')
        if 'apply' in request.POST:
            form = AdminCompletionForm(request.POST)
            if form.is_valid():
                txid = form.cleaned_data['txid']
                notes = form.cleaned_data['notes']
                updated_count = queryset.update(
                    status='completed',
                    txid=txid,
                    admin_notes=notes
                )
                self.message_user(request, f"{updated_count} withdrawals were marked as completed.", messages.SUCCESS)
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = AdminCompletionForm()

        return render(request, 'admin/actions/admin_completion.html', {'items': queryset, 'form': form})

    @admin.action(description='Withdrawal: Fail & Refund User')
    def fail_and_refund_withdrawal(self, request, queryset):
        # Action to fail a withdrawal and refund the user
        queryset = queryset.filter(transaction_type__in=['withdrawal_crypto', 'withdrawal_p2p'], status='pending')
        refunded_count = 0
        for transaction in queryset:
            try:
                # Refund the amount using the deposit method on the wallet object
                # It should be transaction.wallet.deposit
                transaction.wallet.deposit(
                    amount=transaction.amount + transaction.fee, # Refund original amount + fee
                    transaction_type='withdrawal_refund', # New transaction type for clarity (you may need to add this to TRANSACTION_TYPES)
                    description=f"Refund for failed withdrawal {transaction.transaction_id}",
                    admin_notes="Withdrawal failed by admin and funds refunded to user balance."
                )
                transaction.status = 'failed'
                transaction.admin_notes = "Withdrawal failed by admin and funds refunded to user balance."
                transaction.save()
                refunded_count += 1
            except Exception as e:
                self.message_user(request, f"Error refunding {transaction.transaction_id}: {e}", messages.ERROR)
        if refunded_count > 0:
            self.message_user(request, f"{refunded_count} withdrawals were marked as failed and funds refunded.", messages.WARNING)
