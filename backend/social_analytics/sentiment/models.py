from django.db import models
from messages.models import Message


class SentimentAnalysis(models.Model):
    """Sentiment analysis result for a message"""

    SENTIMENT_CHOICES = [
        ('positive', 'Positivo'),
        ('negative', 'Negativo'),
        ('neutral', 'Neutrale'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='sentiment_analyses')

    # Sentiment results
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    sentiment_score = models.FloatField()  # -1 to 1 (negative to positive)
    confidence = models.FloatField(null=True, blank=True)  # 0 to 1

    # Analysis metadata
    analyzer_used = models.CharField(max_length=50, default='textblob')
    analyzed_at = models.DateTimeField(auto_now_add=True)

    # Additional details
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-analyzed_at']
        verbose_name_plural = 'Sentiment analyses'

    def __str__(self):
        return f"{self.sentiment_label} ({self.sentiment_score:.2f}) - {self.message.text[:50]}"
