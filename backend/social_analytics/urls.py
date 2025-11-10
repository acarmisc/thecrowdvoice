"""
URL configuration for social_analytics project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/channels/', include('channels.urls')),
    path('api/messages/', include('messages.urls')),
    path('api/sentiment/', include('sentiment.urls')),
]
