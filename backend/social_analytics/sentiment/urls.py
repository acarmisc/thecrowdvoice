from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'analyses', views.SentimentAnalysisViewSet, basename='sentiment-analysis')

urlpatterns = [
    path('', include(router.urls)),
    path('analyze/<int:message_id>/', views.analyze_message, name='analyze_message'),
    path('batch-analyze/', views.batch_analyze, name='batch_analyze'),
    path('stats/', views.sentiment_stats, name='sentiment_stats'),
]
