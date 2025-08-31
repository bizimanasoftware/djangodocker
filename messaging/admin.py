from django.contrib import admin
from .models import Thread, ChatMessage

# You can register your models with the admin site here.
# This makes them visible and manageable in the Django admin dashboard.

# Register the Thread model to the admin site
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    # This will display the participants and the date in the list view
    list_display = ('participant1', 'participant2', 'updated', 'created')
    # This allows you to search for threads by the usernames of the participants
    search_fields = ('participant1__username', 'participant2__username')

# Register the ChatMessage model to the admin site
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    # This will display the sender, thread, and creation date in the list view
    list_display = ('sender', 'thread', 'created')
    # This allows you to search messages by the sender's username or the message text
    search_fields = ('sender__username', 'text')
    # Adds a date hierarchy for easy filtering by date
    date_hierarchy = 'created'
