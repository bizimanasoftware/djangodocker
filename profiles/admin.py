# /home/deploy/gloexproject/profiles/admin.py
# Configures the Django admin interface for the profiles app.

from django.contrib import admin
from .models import Profile, ProfileGallery, SponsorshipRequest, PaymentLink, CryptoWallet, ProfileComment

class PaymentLinkInline(admin.TabularInline):
    model = PaymentLink
    extra = 1

class CryptoWalletInline(admin.TabularInline):
    model = CryptoWallet
    extra = 1
    max_num = 5

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'category', 'city', 'country', 'is_public')
    list_filter = ('is_public', 'category', 'country')
    search_fields = ('user__username', 'headline', 'bio', 'city')
    raw_id_fields = ('user',)
    inlines = [PaymentLinkInline, CryptoWalletInline]

@admin.register(ProfileComment)
class ProfileCommentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'comment', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('profile__user__username', 'name', 'comment')
    list_editable = ('is_approved',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

@admin.register(ProfileGallery)
class ProfileGalleryAdmin(admin.ModelAdmin):
    list_display = ('profile', 'uploaded_at', 'is_public')
    search_fields = ('profile__user__username',)
    raw_id_fields = ('profile',)

@admin.register(SponsorshipRequest)
class SponsorshipRequestAdmin(admin.ModelAdmin):
    list_display = ('profile', 'requester_name', 'action', 'created_at', 'is_read')
    list_filter = ('action', 'is_read', 'created_at')
    search_fields = ('profile__user__username', 'requester_name', 'requester_email', 'purpose')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
