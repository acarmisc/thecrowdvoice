"""
Sentiment analysis using TextBlob
"""
from textblob import TextBlob
from .models import SentimentAnalysis
from django.utils import timezone


def analyze_sentiment(message):
    """
    Analyze sentiment of a message using TextBlob

    Returns:
        SentimentAnalysis object
    """
    try:
        # Analyze text
        blob = TextBlob(message.text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1

        # Determine sentiment label
        if polarity > 0.1:
            sentiment_label = 'positive'
        elif polarity < -0.1:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'

        # Create sentiment analysis record
        sentiment_analysis = SentimentAnalysis.objects.create(
            message=message,
            sentiment_label=sentiment_label,
            sentiment_score=polarity,
            confidence=abs(polarity),  # Use polarity as confidence
            analyzer_used='textblob',
            details={
                'polarity': polarity,
                'subjectivity': subjectivity,
            }
        )

        # Mark message as processed
        message.is_processed = True
        message.processed_at = timezone.now()
        message.save()

        return sentiment_analysis

    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None


def batch_analyze_messages(messages):
    """
    Analyze sentiment for multiple messages

    Args:
        messages: QuerySet of Message objects

    Returns:
        List of SentimentAnalysis objects
    """
    results = []

    for message in messages:
        # Skip if already analyzed
        if message.is_processed:
            continue

        result = analyze_sentiment(message)
        if result:
            results.append(result)

    return results
