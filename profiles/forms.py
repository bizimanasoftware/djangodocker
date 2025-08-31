# /home/deploy/gloexproject/profiles/forms.py
# Contains all forms used in the profiles application.

from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import (
    Profile, ProfileGallery, SponsorshipRequest, PaymentLink, 
    CryptoWallet, ProfileComment
)

class ProfileForm(forms.ModelForm):
    """ Form for users to edit their main profile details. """
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 'headline', 'bio', 'category', 'city', 'country',
            'contact_email', 'website_url',
            'facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url',
            'languages', 'profile_video', 'is_public'
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Freelance Graphic Designer'}),
            'bio': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Art, Charity, Technology'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/...'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., English, French, Spanish'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Formsets for managing multiple payment and crypto links on the edit page.
PaymentLinkFormSet = inlineformset_factory(
    Profile, PaymentLink,
    fields=('payment_type', 'details'),
    extra=1, can_delete=True,
    widgets={
        'payment_type': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        'details': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
    }
)

CryptoWalletFormSet = inlineformset_factory(
    Profile, CryptoWallet,
    fields=('crypto_type', 'address'),
    extra=1, can_delete=True, max_num=5,
    widgets={
        'crypto_type': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        'address': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
    }
)

class ProfileCommentForm(forms.ModelForm):
    """ Form for submitting a public comment for moderation. """
    class Meta:
        model = ProfileComment
        fields = ['name', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Your Name'}),
            'comment': forms.Textarea(attrs={'class': 'form-control mb-2', 'placeholder': 'Write your comment...', 'rows': 3}),
        }

class ProfileGalleryForm(forms.ModelForm):
    class Meta:
        model = ProfileGallery
        fields = ['image']

ProfileGalleryFormSet = modelformset_factory(
    ProfileGallery, form=ProfileGalleryForm,
    fields=('image',), extra=1, max_num=20, can_delete=True
)

class SponsorshipRequestForm(forms.ModelForm):
    class Meta:
        model = SponsorshipRequest
        fields = ['requester_name', 'requester_email', 'purpose']
        widgets = {
            'requester_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'requester_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'purpose': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'What is your proposal?'}),
        }
