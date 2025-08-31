# wallet/models.py (UPDATED FOR DIRECT CRYPTO SPONSORSHIP AND CAMPAIGN DONATIONS)
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

# Get the User model from settings
User = settings.AUTH_USER_MODEL

# Forward reference for the EmergencyCampaign model
# This prevents a circular import error. The string 'emergencies.EmergencyCampaign' is used.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=18, decimal_places=8, default=Decimal('0.00000000'),
                                     validators=[MinValueValidator(Decimal('0.0'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet (Balance: {self.balance})"

    def update_balance(self, amount, is_credit=True):
        """
        Helper method to update wallet balance.
        is_credit=True means deposit, False means withdrawal/debit.
        Ensures Decimal arithmetic.
        """
        amount = Decimal(str(amount)) # Convert to Decimal to prevent float issues
        if is_credit:
            self.balance += amount
        else:
            if self.balance - amount < Decimal('0.0'):
                raise ValueError("Insufficient balance for this transaction.")
            self.balance -= amount
        self.save()

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit_crypto', 'Crypto Deposit'),
        ('deposit_p2p', 'P2P Deposit'),
        ('sponsorship_deposit', 'Sponsorship Deposit (Manual)'),
        ('sponsorship_crypto', 'Sponsorship Deposit (Crypto)'),
        ('emergency_donation_crypto', 'Emergency Donation (Crypto)'), # NEW TYPE
        ('withdrawal_crypto', 'Crypto Withdrawal'),
        ('withdrawal_p2p', 'P2P Withdrawal'),
        ('internal_transfer_send', 'Internal Transfer (Sent)'),
        ('internal_transfer_receive', 'Internal Transfer (Received)'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('awaiting_admin_instructions', 'Awaiting Admin Instructions'),
        ('awaiting_proof_of_payment', 'Awaiting Proof of Payment'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('expired', 'Expired'),
    )

    # The wallet of the user receiving the funds. For donations/sponsorships, this is the recipient.
    # Can be null for anonymous donations that don't credit a specific user's wallet.
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=18, decimal_places=8, validators=[MinValueValidator(Decimal('0.00000001'))])
    fee = models.DecimalField(max_digits=10, decimal_places=8, default=Decimal('0.00000000'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # --- CAMPAIGN/SPONSORSHIP FIELDS ---
    # The user who is donating/sponsoring, if they are logged in.
    sponsor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sponsorships_made', help_text="The user who is sponsoring, if they are logged in.")
    sponsor_guest_email = models.EmailField(max_length=254, blank=True, null=True, help_text="The email of a guest sponsor.")
    sponsor_guest_name = models.CharField(max_length=150, blank=True, null=True, help_text="The name of a guest sponsor.")
    
    # Link to an emergency campaign, if this transaction is a donation for it.
    campaign = models.ForeignKey(
        'emergencies.EmergencyCampaign',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='donations'
    )

    # For internal transfers
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_transfers')
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transfers')

    # For crypto transactions
    crypto_currency = models.CharField(max_length=10, blank=True, null=True)
    crypto_address = models.CharField(max_length=255, blank=True, null=True)
    tx_hash = models.CharField(max_length=255, blank=True, null=True)
    nowpayments_payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount_received_crypto = models.DecimalField(
        max_digits=18, decimal_places=8,
        null=True, blank=True,
        help_text="Actual crypto amount received (e.g., BTC, ETH) for deposits. Set by IPN."
    )

    # For P2P transactions
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_details = models.TextField(blank=True, null=True)
    user_proof_of_payment = models.FileField(upload_to='proof_of_payments/', blank=True, null=True)

    # Fields for Admin P2P Management
    admin_payment_instructions = models.TextField(
        blank=True, null=True,
        help_text="Instructions provided by admin for P2P deposit (e.g., admin's bank details, mobile money number)."
    )
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes for admin about this transaction.")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} - {self.get_status_display()} (ID: {self.transaction_id})"

# Signals to create Wallet for new users
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
