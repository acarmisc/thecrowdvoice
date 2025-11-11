from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='social_account.platform', read_only=True)
    sentiment = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            'id', 'platform', 'message_type', 'platform_message_id',
            'sender_id', 'sender_name', 'sender_username',
            'text', 'received_at', 'created_at', 'is_processed',
            'sentiment'
        )
        read_only_fields = ('id', 'created_at')

    def get_sentiment(self, obj):
        # Get latest sentiment analysis if exists
        sentiment_analysis = obj.sentiment_analyses.first()
        if sentiment_analysis:
            return {
                'label': sentiment_analysis.sentiment_label,
                'score': sentiment_analysis.sentiment_score
            }
        return None
