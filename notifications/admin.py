# notifications/admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'message_snippet', 'timestamp', 'read', 'notification_type', 'related_object')
    list_filter = ('read', 'notification_type', 'timestamp', 'recipient', 'sender')
    search_fields = ('message', 'recipient__username', 'sender__username')
    raw_id_fields = ('recipient', 'sender')

    def message_snippet(self, obj):
        return obj.message[:75] + '...' if len(obj.message) > 75 else obj.message
    message_snippet.short_description = 'Message'
