# emails/admin.py

from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from .models import IncomingEmail, EmailDraft, IncomingAttachment

# Define an inline admin for attachments
class IncomingAttachmentInline(admin.TabularInline):
    model = IncomingAttachment
    extra = 0
    fields = ('view_attachment',)
    readonly_fields = ('view_attachment',)

    def view_attachment(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.file.url, obj.filename)
        return "No file"
    view_attachment.short_description = "Attachment"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IncomingEmail)
class IncomingEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'received_at', 'has_attachments')
    list_filter = ('sender', 'recipient', 'received_at')
    search_fields = ('subject', 'sender', 'body_plain')
    
    # Make all fields read-only in the change view
    readonly_fields = [
        'sender', 'recipient', 'subject', 'body_html_preview', 
        'body_plain', 'received_at', 'raw_payload'
    ]
    
    # Add the attachment inline
    inlines = [IncomingAttachmentInline]
    
    fieldsets = (
        ('Email Details', {
            'fields': ('sender', 'recipient', 'subject', 'received_at')
        }),
        ('Content', {
            'fields': ('body_html_preview', 'body_plain')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('raw_payload',),
        }),
    )

    def has_add_permission(self, request):
        return False

    def get_list_display(self, request):
        # Add the reply button to the list view dynamically
        # Note: The 'reply_button' method name is used here as a string.
        return ('subject', 'sender', 'recipient', 'received_at', 'has_attachments', 'reply_button')

    def body_html_preview(self, obj):
        # Safely render HTML body in an iframe to isolate styles
        return format_html(
            '<iframe srcdoc="{}" style="width: 100%; height: 500px; border: 1px solid #ccc;"></iframe>',
            obj.body_html
        )
    body_html_preview.short_description = 'HTML Body'

    def has_attachments(self, obj):
        return obj.attachments.exists()
    has_attachments.boolean = True # Show as a nice icon

    def reply_button(self, obj):
        # Ensure you are using the correct name for your composer URL
        # which we set as 'admin_email_composer' in the project urls.py
        url = reverse('admin_email_composer') + f'?reply_to={obj.id}'
        return format_html('<a class="button" href="{}">Reply</a>', url)
    reply_button.short_description = 'Actions'
    # allow_tags is deprecated in modern Django versions, format_html is preferred and safer.
    
@admin.register(EmailDraft)
class EmailDraftAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient', 'created_by', 'updated_at')
    search_fields = ('subject', 'recipient')
    # You could add actions here to "send" a draft
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('email_composer/', self.admin_view(email_composer_view), name='email_composer'),
        ]
        return custom_urls + urls

# If you have a custom admin site, instantiate it. Otherwise, this shows how to add the URL.
# For simplicity with the default admin, we will add the URL directly in the main urls.py.
