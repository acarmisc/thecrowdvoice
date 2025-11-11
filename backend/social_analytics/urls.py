"""
URL configuration for social_analytics project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('social_analytics.accounts.urls')),
    path('api/channels/', include('social_analytics.channels.urls')),
    path('api/messages/', include('social_analytics.interactions.urls')),
    path('api/sentiment/', include('social_analytics.sentiment.urls')),
]
