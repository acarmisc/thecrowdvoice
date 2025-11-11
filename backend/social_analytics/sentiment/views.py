from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from social_analytics.channels.models import SocialAccount
from social_analytics.interactions.models import Message
from .models import SentimentAnalysis
from .serializers import SentimentAnalysisSerializer
from .analyzer import analyze_sentiment, batch_analyze_messages


class SentimentAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """View sentiment analyses"""
    serializer_class = SentimentAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get sentiment analyses for user's messages
        user_accounts = SocialAccount.objects.filter(user=self.request.user)
        user_messages = Message.objects.filter(social_account__in=user_accounts)
        return SentimentAnalysis.objects.filter(message__in=user_messages)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_message(request, message_id):
    """Analyze sentiment for a specific message"""
    try:
        # Ensure the message belongs to the user
        user_accounts = SocialAccount.objects.filter(user=request.user)
        message = Message.objects.get(id=message_id, social_account__in=user_accounts)
    except Message.DoesNotExist:
        return Response({'error': 'Messaggio non trovato'}, status=status.HTTP_404_NOT_FOUND)

    sentiment_analysis = analyze_sentiment(message)

    if sentiment_analysis:
        serializer = SentimentAnalysisSerializer(sentiment_analysis)
        return Response(serializer.data)
    else:
        return Response({'error': 'Errore durante l\'analisi'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_analyze(request):
    """Batch analyze all unprocessed messages"""
    user_accounts = SocialAccount.objects.filter(user=request.user)
    unprocessed_messages = Message.objects.filter(
        social_account__in=user_accounts,
        is_processed=False
    )

    results = batch_analyze_messages(unprocessed_messages)

    return Response({
        'analyzed': len(results),
        'total_unprocessed': unprocessed_messages.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sentiment_stats(request):
    """Get sentiment statistics for user's messages"""
    user_accounts = SocialAccount.objects.filter(user=request.user)
    user_messages = Message.objects.filter(social_account__in=user_accounts)
    sentiments = SentimentAnalysis.objects.filter(message__in=user_messages)

    total = sentiments.count()
    positive = sentiments.filter(sentiment_label='positive').count()
    negative = sentiments.filter(sentiment_label='negative').count()
    neutral = sentiments.filter(sentiment_label='neutral').count()

    return Response({
        'total': total,
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'positive_percentage': (positive / total * 100) if total > 0 else 0,
        'negative_percentage': (negative / total * 100) if total > 0 else 0,
        'neutral_percentage': (neutral / total * 100) if total > 0 else 0,
    })
