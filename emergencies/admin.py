# emergencies/admin.py

from django.contrib import admin
from django.contrib import messages
from .models import EmergencyCampaign, CampaignImage, PaymentMethod, SponsorMessage, CampaignComment

class CampaignImageInline(admin.TabularInline):
    model = CampaignImage
    extra = 1

class PaymentMethodInline(admin.TabularInline):
    model = PaymentMethod
    extra = 1

class SponsorMessageInline(admin.TabularInline):
    model = SponsorMessage
    extra = 0
    readonly_fields = ('name', 'email', 'phone', 'message', 'timestamp')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(EmergencyCampaign)
class EmergencyCampaignAdmin(admin.ModelAdmin):
    # ADD 'is_featured' to list_display
    list_display = ('title', 'recipient', 'status', 'is_active', 'is_featured', 'goal_amount', 'current_amount', 'end_date')
    search_fields = ('title', 'creator__username', 'recipient__username')
    # ADD 'is_featured' to list_filter
    list_filter = ('status', 'is_active', 'is_featured', 'show_progress_bar')
    prepopulated_fields = {'slug': ('title',)}
    
    readonly_fields = ('progress_percentage', 'is_active')
    inlines = [CampaignImageInline, PaymentMethodInline, SponsorMessageInline]
    actions = ['approve_campaigns', 'reject_campaigns']

    fieldsets = (
        ('Campaign Details', {
            'fields': ('title', 'slug', 'description', 'creator', 'recipient', 'end_date')
        }),
        ('Financials & Control', {
            # ADD 'is_featured' to this fieldset
            'fields': ('goal_amount', 'current_amount', 'progress_percentage', 'show_progress_bar', 'is_featured')
        }),
        ('Media & Contact', {
            'fields': ('main_image', 'video_url', 'contact_email', 'contact_phone', 'country', 'city')
        }),
        ('Status', {
            'fields': ('status', 'is_active')
        }),
    )

    @admin.action(description='Approve selected campaigns and make them active')
    def approve_campaigns(self, request, queryset):
        updated_count = queryset.update(status=EmergencyCampaign.CampaignStatus.ACTIVE)
        self.message_user(request, f"{updated_count} campaigns have been approved.", messages.SUCCESS)

    @admin.action(description='Reject selected campaigns')
    def reject_campaigns(self, request, queryset):
        updated_count = queryset.update(status=EmergencyCampaign.CampaignStatus.REJECTED)
        self.message_user(request, f"{updated_count} campaigns have been rejected.", messages.WARNING)

# Register other models for admin visibility
admin.site.register(PaymentMethod)
admin.site.register(SponsorMessage)
admin.site.register(CampaignComment)
