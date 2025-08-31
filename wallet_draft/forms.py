# wallet/forms.py
from django import forms
from .models import Transaction, Wallet
from django.contrib.auth import get_user_model
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class BaseWalletForm(forms.Form):
    """
    Base form to automatically inject the user's wallet instance
    for validation purposes (e.g., checking balance).
    This now explicitly handles 'user_wallet' or 'sender_wallet' if passed directly.
    """
    def __init__(self, *args, **kwargs):
        self.user_wallet = kwargs.pop('user_wallet', None)
        if not self.user_wallet:
            self.user_wallet = kwargs.pop('sender_wallet', None)

        user_instance = kwargs.pop('user', None)

        if not self.user_wallet and user_instance and user_instance.is_authenticated:
            try:
                self.user_wallet = user_instance.wallet
            except Wallet.DoesNotExist:
                logger.warning(f"User {user_instance.username} does not have a wallet.")

        super().__init__(*args, **kwargs)


class CryptoDepositForm(forms.Form): 
    amount = forms.DecimalField(
        label="Amount (USD)",
        max_digits=18, decimal_places=2,
        min_value=Decimal('1.00'),
        help_text="Enter amount in USD. The specific minimum for your chosen crypto will be shown below."
    )
    crypto_currency = forms.ChoiceField(
        label="Cryptocurrency",
        choices=[], 
        help_text="Choose the cryptocurrency for your deposit."
    )
    message = forms.CharField( # This field is for the user's optional message for the deposit
        label="Your Note (Optional)",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Optional message for your records related to this deposit."
    )

    def __init__(self, *args, **kwargs):
        self.crypto_choices = kwargs.pop('crypto_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['crypto_currency'].choices = self.crypto_choices


class P2PDepositRequestForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'payment_method', 'payment_details', 'description']
        widgets = {
            'payment_details': forms.Textarea(attrs={'rows': 4}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'amount': 'Deposit Amount (USD)',
            'payment_method': 'Your Preferred Deposit Method',
            'payment_details': 'Your Account Details (e.g., Bank Account No., Mobile No.)',
            'description': 'Notes for Admin (Optional)',
        }

    payment_method = forms.ChoiceField(
        choices=[
            ('bank_transfer', 'Bank Transfer'),
            ('mobile_money', 'Mobile Money (e.g., MTN, Airtel)'),
            ('e_wallet', 'E-Wallet (e.g., PayPal, Skrill)'),
            ('other', 'Other (specify in notes)'),
        ]
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= Decimal('0'):
            raise forms.ValidationError("Deposit amount must be positive.")
        return amount

class P2PDepositUploadProofForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user_proof_of_payment']
        labels = {'user_proof_of_payment': 'Upload Proof (Image File)'}
        widgets = {'user_proof_of_payment': forms.ClearableFileInput()}

    def clean_user_proof_of_payment(self):
        proof = self.cleaned_data.get('user_proof_of_payment')
        if not proof:
            raise forms.ValidationError("Please select a file to upload.")
        return proof

class InternalTransferForm(BaseWalletForm): 
    recipient_username = forms.CharField(label="Recipient Username", max_length=150)
    amount = forms.DecimalField(label="Amount (USD)", max_digits=18, decimal_places=8)
    description = forms.CharField(
        label="Description (Optional)",
        max_length=255, required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Optional message for the recipient about this transfer."
    )

    def clean_recipient_username(self):
        username = self.cleaned_data.get('recipient_username')
        if not username:
            raise forms.ValidationError("Recipient username is required.")

        try:
            recipient = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Recipient username does not exist.")

        self.recipient_user = recipient

        if self.user_wallet and recipient.wallet == self.user_wallet:
            raise forms.ValidationError("You cannot transfer funds to yourself.")

        if not hasattr(recipient, 'wallet'):
            raise forms.ValidationError(f"Recipient '{username}' does not have an active wallet.")

        return recipient

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not (amount and amount > Decimal('0')):
            raise forms.ValidationError("Transfer amount must be positive.")

        if self.user_wallet and amount > self.user_wallet.balance:
            raise forms.ValidationError("Insufficient balance for this transfer.")

        return amount

class CryptoWithdrawalForm(BaseWalletForm): 
    amount = forms.DecimalField(label="Withdrawal Amount (USD)", max_digits=18, decimal_places=2)
    crypto_currency = forms.ChoiceField(
        label="Withdraw to Cryptocurrency",
        choices=[
            ('btc', 'Bitcoin (BTC)'),
            ('eth', 'Ethereum (ETH)'),
            ('usdttrc20', 'Tether (USDT on Tron/TRC20)'),
            ('usdtbep20', 'Tether (USDT on BSC/BEP20)'),
            ('ltc', 'Litecoin (LTC)'),
        ],
        help_text="Select the cryptocurrency you wish to receive."
    )
    crypto_address = forms.CharField(label="Your Crypto Wallet Address", max_length=255, help_text="Provide the exact wallet address for the chosen cryptocurrency.")
    description = forms.CharField(label="Note (Optional)", required=False, widget=forms.Textarea(attrs={'rows': 3}))

    def __init__(self, *args, **kwargs):
        self.min_withdrawal_amount = kwargs.pop('min_withdrawal_amount', Decimal('0.00'))
        super().__init__(*args, **kwargs)
        self.fields['amount'].help_text = f"Minimum withdrawal: ${self.min_withdrawal_amount:.2f} USD."

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount: return None

        if amount < self.min_withdrawal_amount:
            raise forms.ValidationError(f"Minimum withdrawal amount is ${self.min_withdrawal_amount:.2f}.")

        if self.user_wallet and amount > self.user_wallet.balance:
            raise forms.ValidationError("Insufficient balance for this withdrawal.")

        return amount

class P2PWithdrawalRequestForm(BaseWalletForm): 
    amount = forms.DecimalField(label="Withdrawal Amount (USD)", max_digits=18, decimal_places=2)
    payment_method = forms.ChoiceField(
        label="Preferred Withdrawal Method",
        choices=[
            ('bank_transfer', 'Bank Transfer'),
            ('mobile_money', 'Mobile Money'),
            ('e_wallet', 'E-Wallet'),
            ('other', 'Other (specify in details)'),
        ],
        help_text="Choose how you want to receive your funds."
    )
    recipient_account_details = forms.CharField(
        label="Your Account Details for Receiving Funds",
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="e.g., Bank Name, Account Number, Account Holder Name, Mobile Money Number, E-Wallet ID."
    )
    description = forms.CharField(label="Notes for Admin (Optional)", required=False, widget=forms.Textarea(attrs={'rows': 3}))

    def __init__(self, *args, **kwargs):
        self.min_withdrawal_amount = kwargs.pop('min_withdrawal_amount', Decimal('0.00'))
        super().__init__(*args, **kwargs)
        self.fields['amount'].help_text = f"Minimum withdrawal: ${self.min_withdrawal_amount:.2f} USD."

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount: return None

        if amount < self.min_withdrawal_amount:
            raise forms.ValidationError(f"Minimum withdrawal amount is ${self.min_withdrawal_amount:.2f}.")

        if self.user_wallet and amount > self.user_wallet.balance:
            raise forms.ValidationError("Insufficient balance for this withdrawal.")

        return amount

    def clean_recipient_account_details(self):
        details = self.cleaned_data.get('recipient_account_details')
        if not details:
            raise forms.ValidationError("Please provide your account details for receiving funds.")
        return details


class CryptoDonationForm(BaseWalletForm, CryptoDepositForm): 
    donor_name = forms.CharField(label="Your Name (Optional)", max_length=150, required=False, help_text="Your name will be displayed publicly (or anonymously if left blank) on donation records.")
    # 'amount', 'crypto_currency', 'message' are inherited from CryptoDepositForm.
    # We'll rename 'message' in the view or template for 'Notes for Charity' if desired.

    def __init__(self, *args, **kwargs):
        crypto_choices = kwargs.pop('crypto_choices', [])
        
        # Call the __init__ of the next class in the MRO (BaseWalletForm), then CryptoDepositForm's through super
        super().__init__(*args, **kwargs)

        if 'crypto_currency' in self.fields:
            self.fields['crypto_currency'].choices = crypto_choices
        
        # Override the label for the 'message' field from CryptoDepositForm for clarity in donation context
        if 'message' in self.fields:
            self.fields['message'].label = "Notes for the Cause (Optional)"
            self.fields['message'].help_text = "Add an optional message or dedication for your donation."


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not (amount and amount > Decimal('0')):
            raise forms.ValidationError("Donation amount must be positive.")
        
        if self.user_wallet and amount > self.user_wallet.balance:
            raise forms.ValidationError("Insufficient balance for this donation.")

        return amount

class AdminInstructionForm(forms.Form):
    instructions = forms.CharField(widget=forms.Textarea, label="Payment Instructions for User")

class AdminCompletionForm(forms.Form):
    txid = forms.CharField(label="Blockchain Transaction ID (Optional)", required=False)
    notes = forms.CharField(widget=forms.Textarea, label="Admin Notes (Optional)", required=False)
