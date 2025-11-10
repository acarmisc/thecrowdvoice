from django.contrib import admin
from .models import SocialAccount


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'platform_username', 'status', 'created_at', 'last_sync_at')
    list_filter = ('platform', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'platform_username', 'platform_user_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Account Info', {
            'fields': ('user', 'platform', 'platform_user_id', 'platform_username')
        }),
        ('Status', {
            'fields': ('status', 'last_sync_at')
        }),
        ('Tokens', {
            'fields': ('access_token', 'refresh_token', 'token_expires_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('profile_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
