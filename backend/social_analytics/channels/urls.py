from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.SocialAccountViewSet, basename='social-account')

urlpatterns = [
    path('', include(router.urls)),

    # Facebook OAuth
    path('facebook/auth-url/', views.facebook_auth_url, name='facebook_auth_url'),
    path('facebook/callback/', views.facebook_callback, name='facebook_callback'),

    # Instagram OAuth
    path('instagram/auth-url/', views.instagram_auth_url, name='instagram_auth_url'),

    # LinkedIn OAuth
    path('linkedin/auth-url/', views.linkedin_auth_url, name='linkedin_auth_url'),

    # TikTok OAuth
    path('tiktok/auth-url/', views.tiktok_auth_url, name='tiktok_auth_url'),
]
