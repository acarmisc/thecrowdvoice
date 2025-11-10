from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'social_account', 'message_type', 'sender_name', 'text_preview', 'received_at', 'is_processed')
    list_filter = ('message_type', 'is_processed', 'received_at', 'social_account__platform')
    search_fields = ('text', 'sender_name', 'sender_username', 'platform_message_id')
    readonly_fields = ('created_at', 'updated_at', 'processed_at')
    ordering = ('-received_at',)

    fieldsets = (
        ('Message Info', {
            'fields': ('social_account', 'message_type', 'platform_message_id', 'platform_conversation_id')
        }),
        ('Sender', {
            'fields': ('sender_id', 'sender_name', 'sender_username')
        }),
        ('Content', {
            'fields': ('text', 'raw_data')
        }),
        ('Processing', {
            'fields': ('is_processed', 'processed_at')
        }),
        ('Timestamps', {
            'fields': ('received_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Testo'
