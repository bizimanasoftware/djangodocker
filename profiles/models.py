# /home/deploy/gloexproject/profiles/models.py
# Defines the database structure for user profiles and related data.

from django.db import models
from cloudinary.models import CloudinaryField
from accounts.models import CustomUser

class Profile(models.Model):
    """ Represents a user's profile, extending the CustomUser model. """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # Main Info
    headline = models.CharField(max_length=120, blank=True, help_text='A short, punchy sentence about what you do or need.')
    profile_picture = CloudinaryField(
        'image', folder='profile_pictures',
        transformation={'width': 400, 'height': 400, 'crop': 'fill'},
        blank=True, null=True
    )
    bio = models.TextField(blank=True, help_text="Tell your story, describe your skills, or explain your project.")
    category = models.CharField(max_length=100, default="General", help_text="Your primary category, talent, or tag.")
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Contact & Media
    contact_email = models.EmailField(max_length=255, blank=True, help_text="A public email for sponsors to contact you.")
    website_url = models.URLField(blank=True, help_text="Link to your personal website, portfolio, or project page.")
    profile_video = CloudinaryField(
        'video', resource_type='video', folder='profile_videos',
        blank=True, null=True
    )

    # Social Media Links
    facebook_url = models.URLField(blank=True, help_text="Link to your Facebook profile.")
    twitter_url = models.URLField(blank=True, help_text="Link to your Twitter (X) profile.")
    linkedin_url = models.URLField(blank=True, help_text="Link to your LinkedIn profile.")
    instagram_url = models.URLField(blank=True, help_text="Link to your Instagram profile.")
    
    # Other Optional Fields
    languages = models.CharField(max_length=200, blank=True, help_text="Languages you speak, separated by commas.")
    is_public = models.BooleanField(default=False, help_text="Make your profile visible on the public Discover page.")

    def __str__(self):
        return f"{self.user.username}'s Profile"

class PaymentLink(models.Model):
    """ Stores a custom payment link or detail for a profile. """
    PAYMENT_CHOICES = [
        ('PayPal', 'PayPal'), ('Payoneer', 'Payoneer'), ('Eversend', 'Eversend'),
        ('M-Pesa', 'M-Pesa'), ('Mobile Money', 'Mobile Money'),
        ('Bank Account', 'Bank Account'), ('Other', 'Other'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='payment_links')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    details = models.CharField(max_length=255, help_text="Enter your email, phone number, account number, or a URL.")

    def __str__(self):
        return f"{self.get_payment_type_display()} for {self.profile.user.username}"

class CryptoWallet(models.Model):
    """ Stores a cryptocurrency wallet address for a profile. """
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin (BTC)'), ('ETH', 'Ethereum (ETH)'),
        ('USDT-TRC20', 'Tether (USDT-TRC20)'), ('BNB', 'Binance Coin (BNB)'),
        ('SOL', 'Solana (SOL)'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='crypto_wallets')
    crypto_type = models.CharField(max_length=50, choices=CRYPTO_CHOICES)
    address = models.CharField(max_length=255, help_text="Enter your public wallet address.")

    class Meta:
        unique_together = ('profile', 'crypto_type')

    def __str__(self):
        return f"{self.get_crypto_type_display()} wallet for {self.profile.user.username}"

class ProfileComment(models.Model):
    """ Stores comments made on a user's profile. """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Comments are visible only after approval.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.profile.user.username}'s profile"

class ProfileGallery(models.Model):
    """ Stores multiple gallery images for a user's profile. """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='gallery_images')
    image = CloudinaryField('image', folder='profile_gallery', transformation={'width': 1024, 'height': 768, 'crop': 'limit'})
    is_public = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Profile Galleries"
        ordering = ['-uploaded_at']

class SponsorshipRequest(models.Model):
    """ Stores requests made to a profile owner (e.g., sponsor, donate, connect). """
    ACTION_CHOICES = [('sponsor', 'Sponsor'), ('donate', 'Donate'), ('connect', 'Connect'), ('hire', 'Hire')]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sponsorship_requests')
    requester_name = models.CharField(max_length=255)
    requester_email = models.EmailField()
    purpose = models.TextField(help_text="Briefly explain the purpose of your request.")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
