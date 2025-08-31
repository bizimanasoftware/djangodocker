import uuid
from decimal import Decimal
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models import F # Import F expression for atomic updates

User = get_user_model()

class Wallet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(
        max_digits=18,
        decimal_places=8,
        default=Decimal('0.00000000'),
        validators=[MinValueValidator(Decimal('0.00000000'))]
    )
    currency = models.CharField(max_length=10, default='USD') # Base currency for the wallet

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.username}'s Wallet ({self.balance} {self.currency})"

    @transaction.atomic
    def deposit(self, amount, transaction_type, description=None, crypto_currency=None,
                nowpayments_payment_id=None, nowpayments_pay_amount=None,
                payment_method=None, admin_payment_instructions=None,
                user_proof_of_payment=None, admin_notes=None, payment_details=None):
        """
        Deposits funds into the wallet within an atomic transaction, using select_for_update
        and F() expressions for race-condition-proof balance updates.
        Returns the created transaction object.
        """
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        # Lock the wallet row for update to prevent race conditions
        # We fetch the wallet instance again within the atomic block
        wallet_to_update = Wallet.objects.select_for_update().get(pk=self.pk)

        # Determine initial status based on transaction type
        initial_status = 'pending'
        if transaction_type in ['internal_transfer_receive', 'initial_deposit', 'deposit_fiat']:
            initial_status = 'completed'
        elif transaction_type == 'crypto_deposit':
            initial_status = 'awaiting_confirmation' # Awaiting blockchain confirmation
        elif transaction_type == 'p2p_deposit':
            if not admin_payment_instructions:
                initial_status = 'awaiting_admin_instructions'
            else:
                initial_status = 'awaiting_proof_of_payment'

        # Create the transaction record first
        deposit_transaction = Transaction.objects.create(
            wallet=wallet_to_update, # Use the locked wallet instance
            transaction_type=transaction_type,
            amount=amount,
            status=initial_status,
            description=description,
            crypto_currency=crypto_currency,
            nowpayments_payment_id=nowpayments_payment_id,
            nowpayments_pay_address=nowpayments_pay_address, # Make sure this is passed if needed
            nowpayments_pay_amount=nowpayments_pay_amount,
            payment_method=payment_method,
            admin_payment_instructions=admin_payment_instructions,
            user_proof_of_payment=user_proof_of_payment,
            admin_notes=admin_notes,
            payment_details=payment_details,
        )

        # Update wallet balance only if the transaction type implies an immediate balance increase
        if transaction_type in ['internal_transfer_receive', 'initial_deposit', 'deposit_fiat']:
            wallet_to_update.balance = F('balance') + amount
            wallet_to_update.save(update_fields=['balance'])
            # Refresh the Python object to reflect the database changes
            wallet_to_update.refresh_from_db()
            # If balance is updated immediately, ensure transaction status is completed
            if deposit_transaction.status != 'completed': # Prevent redundant saves if already completed
                deposit_transaction.status = 'completed'
                deposit_transaction.save(update_fields=['status'])

        # No need for explicit 'elif transaction_type == "p2p_deposit"' block here
        # as status is already set in initial_status and saved with transaction creation.
        # Same for 'crypto_deposit'. The balance for these types is updated via
        # a separate process (e.g., webhook for crypto, admin verification for P2P)

        return deposit_transaction

    @transaction.atomic
    def withdraw(self, amount, transaction_type, description=None, crypto_currency=None,
                 crypto_address=None, payment_method=None, recipient_account_details=None,
                 p2p_proof_of_completion=None, admin_notes=None, withdrawal_fee=Decimal('0.00')):
        """
        Withdraws funds from the wallet within an atomic transaction, using select_for_update
        and F() expressions for race-condition-proof balance updates.
        Returns the created transaction object.
        """
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        total_amount = amount + withdrawal_fee

        # Lock the wallet row for update to prevent race conditions
        wallet_to_update = Wallet.objects.select_for_update().get(pk=self.pk)

        if wallet_to_update.balance < total_amount:
            raise ValueError("Insufficient funds for withdrawal.")

        # Create the transaction record first, status is pending for withdrawals
        withdrawal_transaction = Transaction.objects.create(
            wallet=wallet_to_update, # Use the locked wallet instance
            transaction_type=transaction_type,
            amount=amount,
            status='pending', # Withdrawals are usually pending until processed
            description=description,
            crypto_currency=crypto_currency,
            crypto_address=crypto_address,
            payment_method=payment_method,
            recipient_account_details=recipient_account_details,
            p2p_proof_of_completion=p2p_proof_of_completion,
            admin_notes=admin_notes,
            fee=withdrawal_fee,
        )

        # Immediately deduct funds from the balance for pending withdrawals
        # The funds are "locked" or "held" for the withdrawal
        wallet_to_update.balance = F('balance') - total_amount
        wallet_to_update.save(update_fields=['balance'])
        # Refresh the Python object to reflect the database changes
        wallet_to_update.refresh_from_db()

        return withdrawal_transaction

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('initial_deposit', 'Initial Deposit'),
        ('crypto_deposit', 'Crypto Deposit'),
        ('p2p_deposit', 'P2P Deposit'),
        ('deposit_fiat', 'Fiat Deposit'), # Added this missing type
        ('internal_transfer_send', 'Internal Transfer (Sent)'),
        ('internal_transfer_receive', 'Internal Transfer (Received)'),
        ('withdrawal_crypto', 'Crypto Withdrawal'),
        ('withdrawal_p2p', 'P2P Withdrawal'),
        ('donation', 'Donation'),
        # Add other transaction types as needed, e.g., 'purchase', 'refund'
    )

    TRANSACTION_STATUSES = (
        ('pending', 'Pending'), # For withdrawals awaiting processing
        ('completed', 'Completed'), # Transaction successfully processed
        ('failed', 'Failed'), # Transaction failed
        ('cancelled', 'Cancelled'), # Transaction cancelled by user or admin
        ('awaiting_confirmation', 'Awaiting Confirmation'), # For crypto deposits awaiting blockchain confirmation
        ('awaiting_proof_of_payment', 'Awaiting Proof of Payment'), # For P2P deposits, waiting for user to upload proof
        ('awaiting_admin_instructions', 'Awaiting Admin Instructions'), # For P2P deposits, waiting for admin to provide details
        ('in_review', 'In Review'), # Proof of payment uploaded, awaiting admin review (for P2P)
    )

    PAYMENT_METHODS = (
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bitcoin', 'Bitcoin'),
        ('ethereum', 'Ethereum'),
        ('usdt_trc20', 'USDT (TRC20)'),
        ('usdt_erc20', 'USDT (ERC20)'),
        ('litecoin', 'Litecoin'),
        ('dogecoin', 'Dogecoin'),
        # Add other methods
    )

    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=18, decimal_places=8, validators=[MinValueValidator(Decimal('0.00000001'))])
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUSES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    fee = models.DecimalField(max_digits=18, decimal_places=8, default=Decimal('0.00000000'))

    # Fields for Crypto Transactions (Deposits and Withdrawals)
    crypto_currency = models.CharField(max_length=20, blank=True, null=True)
    crypto_address = models.CharField(max_length=100, blank=True, null=True) # Destination address for withdrawals
    nowpayments_payment_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    nowpayments_pay_address = models.CharField(max_length=255, blank=True, null=True) # Address to send crypto to for deposit
    nowpayments_pay_amount = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    nowpayments_order_id = models.CharField(max_length=255, blank=True, null=True) # Your internal order ID for NowPayments

    # Fields for P2P Transactions (Deposits and Withdrawals)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, blank=True, null=True)
    # NEW FIELD: Details about the user's account from which they are sending the P2P deposit
    payment_details = models.TextField(blank=True, null=True, help_text="Details of the user's account used to send the payment (e.g., bank name, account number, mobile money number).")
    # For P2P withdrawals: details where user wants money sent (e.g., bank account number)
    recipient_account_details = models.TextField(blank=True, null=True)
    # For P2P deposits: user uploads proof they sent money
    user_proof_of_payment = models.FileField(upload_to='p2p_proofs/', blank=True, null=True)
    # For P2P withdrawals: admin uploads proof they sent money
    admin_proof_of_payout = models.FileField(upload_to='admin_payout_proofs/', blank=True, null=True)
    # For P2P: instructions from admin to user for deposits
    admin_payment_instructions = models.TextField(blank=True, null=True)
    # For P2P: proof user provides for withdrawal (e.g. screenshot of receipt)
    p2p_proof_of_completion = models.FileField(upload_to='p2p_completion_proofs/', blank=True, null=True) # Corrected null=2 to null=True

    # Fields for Internal Transfers
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_transfers')
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transfers')

    # Admin notes for any transaction
    admin_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp'] # Order by most recent first

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.amount} {self.wallet.currency} for {self.wallet.owner.username} (Status: {self.get_status_display()})"

    def get_transaction_type_display(self):
        return dict(Transaction.TRANSACTION_TYPES).get(self.transaction_type, self.transaction_type)

    def get_status_display(self):
        return dict(Transaction.TRANSACTION_STATUSES).get(self.status, self.status)

    def get_payment_method_display(self):
        return dict(Transaction.PAYMENT_METHODS).get(self.payment_method, self.payment_method)

    # Property to easily check if it's a deposit
    @property
    def is_deposit(self):
        return self.transaction_type in ['crypto_deposit', 'p2p_deposit', 'initial_deposit', 'internal_transfer_receive', 'deposit_fiat']

    # Property to easily check if it's a withdrawal
    @property
    def is_withdrawal(self):
        return self.transaction_type in ['withdrawal_crypto', 'withdrawal_p2p', 'internal_transfer_send']

    # Property to easily check if it's an internal transfer (either send or receive)
    @property
    def is_internal_transfer(self):
        return self.transaction_type in ['internal_transfer_send', 'internal_transfer_receive']
