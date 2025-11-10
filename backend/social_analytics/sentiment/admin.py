from django.contrib import admin
from .models import SentimentAnalysis


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('message', 'sentiment_label', 'sentiment_score', 'confidence', 'analyzer_used', 'analyzed_at')
    list_filter = ('sentiment_label', 'analyzer_used', 'analyzed_at')
    search_fields = ('message__text', 'message__sender_name')
    readonly_fields = ('analyzed_at',)
    ordering = ('-analyzed_at',)

    fieldsets = (
        ('Message', {
            'fields': ('message',)
        }),
        ('Sentiment', {
            'fields': ('sentiment_label', 'sentiment_score', 'confidence')
        }),
        ('Analysis', {
            'fields': ('analyzer_used', 'analyzed_at', 'details')
        }),
    )
