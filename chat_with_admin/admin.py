# chat_with_admin/admin.py
from django.contrib import admin
from django.contrib import messages as django_messages
from django.template.defaultfilters import truncatechars
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse

from .models import AdminChatMessage # <--- ADD THIS LINE!

User = get_user_model()


@admin.register(AdminChatMessage)
class AdminChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_link_display', 'sender_info_display', 'message_preview',
        'timestamp', 'is_read_by_user', 'is_read_by_admin',
    )
    list_filter = (
        'sender_is_admin', 'is_read_by_user', 'is_read_by_admin',
        'timestamp', 'user', 'anonymous_sender_name', 'anonymous_sender_email',
    )
    search_fields = (
        'message', 'user__username', 'user__email',
        'anonymous_sender_name', 'anonymous_sender_email',
    )
    # raw_id_fields = ('user',)
    readonly_fields = ('timestamp',)

    fieldsets = (
        (None, {
            'fields': ('user', 'anonymous_sender_name', 'anonymous_sender_email', 'sender_is_admin', 'message')
        }),
        ('Status', {
            'fields': ('is_read_by_user', 'is_read_by_admin', 'timestamp')
        }),
    )

    def user_link_display(self, obj):
        if obj.user:
            try:
                user_admin_url = reverse('admin:auth_user_change', args=[obj.user.pk])
                return format_html('<a href="{}">{}</a>', user_admin_url, obj.user.username)
            except Exception:
                return obj.user.username
        return "N/A"
    user_link_display.short_description = 'Registered User'
    user_link_display.admin_order_field = 'user__username'


    def sender_info_display(self, obj):
        if obj.sender_is_admin:
            return "Admin"
        elif obj.user:
            return obj.user.username
        elif obj.anonymous_sender_name and obj.anonymous_sender_email:
            return f"{obj.anonymous_sender_name} ({obj.anonymous_sender_email})"
        elif obj.anonymous_sender_name:
            return obj.anonymous_sender_name
        elif obj.anonymous_sender_email:
            return obj.anonymous_sender_email
        return "Anonymous"
    sender_info_display.short_description = 'Sender'
    sender_info_display.admin_order_field = 'sender_is_admin'

    def message_preview(self, obj):
        return truncatechars(obj.message, 75)
    message_preview.short_description = 'Message'

    actions = ['mark_selected_messages_read_by_admin', 'mark_selected_messages_unread_by_admin',
               'mark_selected_messages_read_by_user', 'mark_selected_messages_unread_by_user',
               'delete_selected_conversations']

    def mark_selected_messages_read_by_admin(self, request, queryset):
        updated = queryset.update(is_read_by_admin=True)
        self.message_user(request, f'{updated} messages marked as read by admin.', level=django_messages.SUCCESS)
    mark_selected_messages_read_by_admin.short_description = "Mark selected messages as read by admin"

    def mark_selected_messages_unread_by_admin(self, request, queryset):
        updated = queryset.update(is_read_by_admin=False)
        self.message_user(request, f'{updated} messages marked as unread by admin.', level=django_messages.SUCCESS)
    mark_selected_messages_unread_by_admin.short_description = "Mark selected messages as unread by admin"

    def mark_selected_messages_read_by_user(self, request, queryset):
        updated = queryset.update(is_read_by_user=True)
        self.message_user(request, f'{updated} messages marked as read by user.', level=django_messages.SUCCESS)
    mark_selected_messages_read_by_user.short_description = "Mark selected messages as read by user"

    def mark_selected_messages_unread_by_user(self, request, queryset):
        updated = queryset.update(is_read_by_user=False)
        self.message_user(request, f'{updated} messages marked as unread by user.', level=django_messages.SUCCESS)
    mark_selected_messages_unread_by_user.short_description = "Mark selected messages as unread by user"

    def delete_selected_conversations(self, request, queryset):
        if not request.user.has_perm('chat_with_admin.delete_adminchatmessage'):
            self.message_user(request, "Sorry, you don't have permission to delete conversations.", level=django_messages.ERROR)
            return

        users_to_delete_for = queryset.values_list('user', flat=True).distinct()
        anonymous_senders_info = queryset.filter(user__isnull=True).values_list('anonymous_sender_name', 'anonymous_sender_email').distinct()

        deleted_count = 0
        deleted_conversations_info = []

        for user_id in users_to_delete_for:
            if user_id is not None:
                try:
                    user_obj = User.objects.get(pk=user_id)
                    messages_in_conversation = AdminChatMessage.objects.filter(user=user_obj)
                    count, _ = messages_in_conversation.delete()
                    deleted_count += count
                    deleted_conversations_info.append(str(user_obj.username))
                except User.DoesNotExist:
                    pass

        anonymous_messages_selected = queryset.filter(user__isnull=True)
        if anonymous_messages_selected.exists():
            for name, email in anonymous_senders_info:
                display_name = name if name else (email if email else "Anonymous Contact")
                if f"Anonymous: {display_name}" not in deleted_conversations_info:
                    deleted_conversations_info.append(f"Anonymous: {display_name}")

            count, _ = anonymous_messages_selected.delete()
            deleted_count += count


        if deleted_count > 0:
            self.message_user(request, f'Successfully deleted {deleted_count} messages across conversation(s)/contacts with: {", ".join(deleted_conversations_info)}', level=django_messages.SUCCESS)
        else:
            self.message_user(request, 'No messages were deleted.', level=django_messages.WARNING)

    delete_selected_conversations.short_description = "Delete entire conversation(s) / selected anonymous messages"


try:
    if hasattr(User, 'can_access_chat'):
        class CustomUserAdmin(BaseUserAdmin):
            fieldsets = BaseUserAdmin.fieldsets + (
                (('Chat Permissions'), {
                    'fields': ('can_access_chat',),
                }),
            )
            list_display = BaseUserAdmin.list_display + ('can_access_chat',)
            list_filter = BaseUserAdmin.list_filter + ('can_access_chat',)

        admin.site.unregister(User)
        admin.site.register(User, CustomUserAdmin)
except Exception as e:
    print(f"Warning: Could not customize UserAdmin for chat permissions: {e}")
