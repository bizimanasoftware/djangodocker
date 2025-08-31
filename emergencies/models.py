# emergencies/models.py

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from decimal import Decimal
from cloudinary.models import CloudinaryField

# This model is no longer used for donations but for tracking messages.
# We will create a new one. The wallet.Transaction is for platform-level transactions.
# from wallet.models import Transaction

class EmergencyCampaign(models.Model):
    """
    Represents an emergency fundraising campaign, now with more user control.
    """
    class CampaignStatus(models.TextChoices):
        PENDING_APPROVAL = 'pending', 'Pending Approval'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        REJECTED = 'rejected', 'Rejected'

    title = models.CharField(max_length=255, help_text="The title of the emergency campaign.")
    description = models.TextField(help_text="A detailed description of the cause.")
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="The target fundraising amount.")
    current_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'),
        help_text="The total amount received. Can be updated manually by the campaign creator or admin."
    )
    main_image = CloudinaryField('image', help_text="The main promotional image for the campaign.", null=True, blank=True)
    video_url = models.URLField(blank=True, null=True, help_text="Optional: A link to a promotional video (e.g., YouTube, Vimeo).")

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="created_campaigns", help_text="The user who submitted the campaign request."
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="beneficiary_campaigns", help_text="The user who is the beneficiary of this campaign."
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(help_text="The date when the campaign will officially end.")
    is_active = models.BooleanField(default=False, help_text="This is automatically set to True when a campaign is approved by an admin.")
    status = models.CharField(max_length=20, choices=CampaignStatus.choices, default=CampaignStatus.PENDING_APPROVAL)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    # New Fields for User Control and Contact
    show_progress_bar = models.BooleanField(default=True, help_text="If checked, the fundraising progress bar will be visible to the public.")
    contact_email = models.EmailField(blank=True, null=True, help_text="Public contact email for this campaign.")
    contact_phone = models.CharField(max_length=30, blank=True, null=True, help_text="Public contact phone number.")
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Check this box to feature the campaign on the homepage."
    )

    class Meta:
        permissions = [("can_request_campaign", "Can request an emergency campaign")]
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.goal_amount and self.goal_amount > 0:
            return min((self.current_amount / self.goal_amount) * 100, 100)
        return 0

    def get_absolute_url(self):
        return reverse('emergencies:campaign_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.is_active = (self.status == self.CampaignStatus.ACTIVE)
        super().save(*args, **kwargs)

class PaymentMethod(models.Model):
    """
    Stores various payment methods a campaign recipient can accept.
    """
    METHOD_CHOICES = [
        ('mobile_money', 'Mobile Money (e.g., MTN, Airtel)'),
        ('mpesa', 'M-Pesa'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('payoneer', 'Payoneer'),
        ('eversend', 'Eversend'),
        ('crypto', 'Cryptocurrency'),
    ]
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin (BTC)'), ('ETH', 'Ethereum (ETH)'), ('USDT', 'Tether (USDT)'),
        ('USDC', 'USD Coin (USDC)'), ('BNB', 'Binance Coin (BNB)'), ('XRP', 'Ripple (XRP)'),
        ('DOGE', 'Dogecoin (DOGE)'),
    ]

    campaign = models.ForeignKey(EmergencyCampaign, on_delete=models.CASCADE, related_name="payment_methods")
    method_type = models.CharField(max_length=50, choices=METHOD_CHOICES)
    
    # Details - fields are selectively used based on method_type
    account_holder_name = models.CharField(max_length=255, blank=True, help_text="Your full name for the account.")
    phone_number = models.CharField(max_length=50, blank=True, help_text="Required for Mobile Money, M-Pesa, etc.")
    email_address = models.EmailField(blank=True, help_text="Your PayPal, Payoneer, or contact email.")
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=100, blank=True, help_text="Or IBAN")
    swift_bic = models.CharField("SWIFT/BIC", max_length=20, blank=True)
    crypto_coin = models.CharField(max_length=10, choices=CRYPTO_CHOICES, blank=True)
    wallet_address = models.CharField(max_length=255, blank=True)
    instructions = models.TextField(blank=True, help_text="Any additional instructions for the donor.")

    def __str__(self):
        return f"{self.get_method_type_display()} for {self.campaign.title}"

class SponsorMessage(models.Model):
    """
    Stores messages sent from potential sponsors/donors to the campaign creator.
    """
    campaign = models.ForeignKey(EmergencyCampaign, on_delete=models.CASCADE, related_name="sponsor_messages")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.name} for {self.campaign.title}"

class CampaignComment(models.Model):
    """
    A public comment on a campaign page.
    """
    campaign = models.ForeignKey(EmergencyCampaign, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.campaign.title}"

class CampaignImage(models.Model):
    """
    Represents an additional gallery image for a campaign.
    """
    campaign = models.ForeignKey(EmergencyCampaign, on_delete=models.CASCADE, related_name="gallery_images")
    image = CloudinaryField('image', help_text="Upload an image for the campaign gallery.")
    caption = models.CharField(max_length=255, blank=True, help_text="Optional caption for the image.")

    def __str__(self):
        return f"Image for {self.campaign.title}"
