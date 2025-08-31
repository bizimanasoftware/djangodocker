# emergencies/forms.py

from django import forms
from django.contrib.auth import get_user_model
from .models import EmergencyCampaign, PaymentMethod, SponsorMessage, CampaignComment

User = get_user_model()

class EmergencyCampaignRequestForm(forms.ModelForm):
    """
    Form for users to request a new emergency campaign.
    """
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        help_text="Set a clear end date for your campaign."
    )
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        label="Campaign Beneficiary",
        help_text="Select the user who will receive the funds from this campaign."
    )

    class Meta:
        model = EmergencyCampaign
        fields = [
            'title', 'recipient', 'description', 'goal_amount', 'end_date',
            'main_image', 'video_url', 'show_progress_bar', 'contact_email',
            'contact_phone', 'country', 'city'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'goal_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/watch?v=...'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'show_progress_bar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CampaignUpdateForm(forms.ModelForm):
    """
    Form for the campaign creator to update their campaign details,
    including manually setting the current amount raised.
    """
    class Meta:
        model = EmergencyCampaign
        fields = ['description', 'current_amount', 'show_progress_bar', 'contact_email', 'contact_phone', 'country', 'city']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'current_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'show_progress_bar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'current_amount': "Manually enter the total amount you have received in your wallets. This will update the progress bar."
        }

class PaymentMethodForm(forms.ModelForm):
    """
    Form for adding/editing payment methods.
    """
    class Meta:
        model = PaymentMethod
        exclude = ['campaign']
        widgets = {
            'method_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_method_type'}),
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'swift_bic': forms.TextInput(attrs={'class': 'form-control'}),
            'crypto_coin': forms.Select(attrs={'class': 'form-select'}),
            'wallet_address': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SponsorMessageForm(forms.ModelForm):
    """
    The new 'contact' form on the campaign detail page.
    """
    class Meta:
        model = SponsorMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone (Optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message to the campaign creator...'}),
        }

class CampaignCommentForm(forms.ModelForm):
    """
    Form for submitting a public comment.
    """
    class Meta:
        model = CampaignComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Leave a public comment...'}),
        }
        labels = {
            'text': ''
        }
