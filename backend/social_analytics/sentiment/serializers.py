from rest_framework import serializers
from .models import SentimentAnalysis


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    message_text = serializers.CharField(source='message.text', read_only=True)

    class Meta:
        model = SentimentAnalysis
        fields = (
            'id', 'message', 'message_text', 'sentiment_label',
            'sentiment_score', 'confidence', 'analyzer_used',
            'analyzed_at', 'details'
        )
        read_only_fields = ('id', 'analyzed_at')
