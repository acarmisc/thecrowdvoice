from django.db import models
from django.conf import settings


class SocialAccount(models.Model):
    """Social media account connected by user"""

    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
    ]

    STATUS_CHOICES = [
        ('active', 'Attivo'),
        ('inactive', 'Inattivo'),
        ('error', 'Errore'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='social_accounts')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    platform_user_id = models.CharField(max_length=255)
    platform_username = models.CharField(max_length=255, blank=True)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Additional metadata
    profile_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'platform', 'platform_user_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.platform} ({self.platform_username})"
