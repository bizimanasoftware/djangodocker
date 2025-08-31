# wallet/forms.py (UPDATED FOR DIRECT CRYPTO SPONSORSHIP)

from django import forms
from .models import Transaction, Wallet
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

# --- ADD THIS LIST ---
# This is the list of crypto choices that the emergencies app needs.
# It defines the supported cryptocurrencies for NOWPayments.
CRYPTO_CURRENCY_CHOICES = [
    ('btc', 'Bitcoin (BTC)'),
    ('eth', 'Ethereum (ETH)'),
    ('ltc', 'Litecoin (LTC)'),
    ('doge', 'Dogecoin (DOGE)'),
    ('usdttrc20', 'Tether (USDT - TRC20)'), # Use network-specific ticker
    ('usdtbep20', 'Tether (USDT - BEP20)'), # Provide multiple network options
    ('sol', 'Solana (SOL)'),
    ('xmr', 'Monero (XMR)'),
]
# --- NEW: DIRECT CRYPTO SPONSORSHIP FORM ---
class CryptoSponsorshipForm(forms.ModelForm):
    """
    A public form for sponsoring a user directly with cryptocurrency via NOWPayments.
    Can be filled by a guest or a logged-in user.
    """
    sponsor_guest_email = forms.EmailField(
        required=True,
        label="Your Email Address",
        help_text="We'll send a confirmation to this address."
    )
    sponsor_guest_name = forms.CharField(
        max_length=150,
        required=False,
        label="Your Name (Optional)"
    )
    crypto_currency = forms.ChoiceField(
        choices=[
            ('btc', 'Bitcoin'),
            ('eth', 'Ethereum'),
            ('usdttrc20', 'USDT (TRC-20)'),
            # Add other currencies supported by NOWPayments as needed
        ],
        label="Choose Cryptocurrency",
        help_text="The currency you will use to pay."
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'crypto_currency', 'sponsor_guest_name', 'sponsor_guest_email', 'description']
        labels = {
            'amount': 'Sponsorship Amount (USD)',
            'description': 'Message to the person you are sponsoring (Optional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Check if the user is authenticated and passed to the form
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If the user is logged in, the email field is not needed
        if self.user and self.user.is_authenticated:
            self.fields['sponsor_guest_email'].required = False
            self.fields['sponsor_guest_email'].widget = forms.HiddenInput()
            # Pre-fill name if available
            self.fields['sponsor_guest_name'].initial = self.user.get_full_name() or self.user.username

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= Decimal('0'):
            raise forms.ValidationError("Sponsorship amount must be greater than zero.")
        return amount

# --- EXISTING MANUAL SPONSORSHIP FORM (Unchanged) ---
class SponsorshipDepositForm(forms.ModelForm):
    """
    A public form for sponsoring a user via manual payment methods.
    """
    sponsor_guest_email = forms.EmailField(
        required=True,
        label="Your Email Address",
        help_text="We will use this to send payment instructions."
    )
    sponsor_guest_name = forms.CharField(
        max_length=150,
        required=False,
        label="Your Name (Optional)"
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('bank_transfer', 'Bank Transfer'),
            ('mobile_money', 'Mobile Money'),
            ('other', 'Other'),
        ],
        label="How would you like to sponsor?",
        help_text="An admin will provide payment details based on your choice."
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'payment_method', 'sponsor_guest_name', 'sponsor_guest_email', 'description']
        labels = {
            'amount': 'Sponsorship Amount (USD)',
            'description': 'Message to the person you are sponsoring (Optional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['sponsor_guest_email'].required = False
            self.fields['sponsor_guest_email'].widget = forms.HiddenInput()
            self.fields['sponsor_guest_name'].initial = self.user.get_full_name() or self.user.username

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= Decimal('0'):
            raise forms.ValidationError("Sponsorship amount must be greater than zero.")
        return amount


# --- OTHER EXISTING FORMS (Unchanged) ---

class BaseWalletForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user', None)
        self.user_wallet = None
        if self.user_instance:
            try:
                self.user_wallet = self.user_instance.wallet
            except Wallet.DoesNotExist:
                pass
        super().__init__(*args, **kwargs)

class CryptoDepositForm(BaseWalletForm):
    amount = forms.DecimalField(max_digits=18, decimal_places=8, min_value=Decimal('0.00000001'), help_text="Amount in USD you wish to deposit.")
    crypto_currency = forms.ChoiceField(choices=[('btc', 'Bitcoin'), ('eth', 'Ethereum'), ('usdttrc20', 'USDT (TRC-20)')], help_text="Choose the cryptocurrency for your deposit.")
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= Decimal('0'):
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return amount

class P2PDepositRequestForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'payment_method', 'payment_details', 'description']
        widgets = {
            'payment_details': forms.Textarea(attrs={'rows': 4}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    payment_method = forms.ChoiceField(choices=[('bank_transfer', 'Bank Transfer'), ('mobile_money', 'Mobile Money'), ('other', 'Other')], label="Preferred Deposit Method")
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= Decimal('0'):
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return amount

class ProofOfPaymentUploadForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user_proof_of_payment']

class InternalTransferForm(BaseWalletForm):
    recipient_username = forms.CharField(max_length=150)
    amount = forms.DecimalField(max_digits=18, decimal_places=8, min_value=Decimal('0.00000001'))
    description = forms.CharField(required=False, widget=forms.Textarea)

    def clean_recipient_username(self):
        username = self.cleaned_data['recipient_username']
        try:
            recipient = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise ValidationError("Recipient does not exist.")
        if recipient == self.user_instance:
            raise ValidationError("You cannot transfer to yourself.")
        if not hasattr(recipient, 'wallet'):
            raise ValidationError("Recipient does not have a wallet.")
        return recipient

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not self.user_wallet:
            raise ValidationError("Your wallet not found.")
        if amount > self.user_wallet.balance:
            raise ValidationError("Insufficient balance.")
        return amount

class CryptoWithdrawalForm(BaseWalletForm):
    amount = forms.DecimalField(max_digits=18, decimal_places=8, min_value=Decimal('0.00000001'))
    crypto_currency = forms.ChoiceField(choices=[('btc', 'Bitcoin'), ('eth', 'Ethereum')])
    crypto_address = forms.CharField(max_length=255)
    description = forms.CharField(required=False, widget=forms.Textarea)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not self.user_wallet:
            raise ValidationError("Your wallet not found.")
        if amount > self.user_wallet.balance:
            raise ValidationError("Insufficient balance.")
        return amount

class P2PWithdrawalRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_wallet = kwargs.pop('user_wallet', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Transaction
        fields = ['amount', 'payment_method', 'payment_details', 'description']

    payment_method = forms.ChoiceField(choices=[('bank_transfer', 'Bank Transfer'), ('mobile_money', 'Mobile Money')])

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not self.user_wallet:
            raise ValidationError("Your wallet not found.")
        if amount > self.user_wallet.balance:
            raise ValidationError("Insufficient balance.")
        return amount
