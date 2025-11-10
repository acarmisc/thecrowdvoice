from django.db import models
from channels.models import SocialAccount


class Message(models.Model):
    """Message/interaction received from social media"""

    MESSAGE_TYPE_CHOICES = [
        ('direct_message', 'Messaggio Diretto'),
        ('comment', 'Commento'),
        ('mention', 'Menzione'),
        ('tag', 'Tag'),
        ('reply', 'Risposta'),
    ]

    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)

    # Message identifiers
    platform_message_id = models.CharField(max_length=255, unique=True)
    platform_conversation_id = models.CharField(max_length=255, blank=True)

    # Sender information
    sender_id = models.CharField(max_length=255)
    sender_name = models.CharField(max_length=255, blank=True)
    sender_username = models.CharField(max_length=255, blank=True)

    # Message content
    text = models.TextField()
    raw_data = models.JSONField(default=dict)  # Store complete platform response

    # Metadata
    received_at = models.DateTimeField()  # When the message was sent on the platform
    created_at = models.DateTimeField(auto_now_add=True)  # When we stored it
    updated_at = models.DateTimeField(auto_now=True)

    # Processing status
    is_processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-received_at']
        indexes = [
            models.Index(fields=['social_account', '-received_at']),
            models.Index(fields=['platform_message_id']),
        ]

    def __str__(self):
        return f"{self.message_type} da {self.sender_name} su {self.social_account.platform}"
