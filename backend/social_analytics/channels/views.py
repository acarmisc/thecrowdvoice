from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
import requests
from .models import SocialAccount
from .serializers import SocialAccountSerializer


class SocialAccountViewSet(viewsets.ModelViewSet):
    serializer_class = SocialAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SocialAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def facebook_auth_url(request):
    """Get Facebook OAuth URL"""
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    scope = 'pages_show_list,pages_read_engagement,pages_manage_metadata,pages_messaging'

    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={settings.FACEBOOK_APP_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&state={request.user.id}"  # Pass user ID for security
    )

    return Response({'auth_url': auth_url})


@api_view(['GET'])
def facebook_callback(request):
    """Handle Facebook OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')  # user_id

    if not code:
        return Response({'error': 'Codice di autorizzazione mancante'}, status=status.HTTP_400_BAD_REQUEST)

    # Exchange code for access token
    token_url = 'https://graph.facebook.com/v18.0/oauth/access_token'
    token_params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
        'code': code
    }

    try:
        token_response = requests.get(token_url, params=token_params)
        token_data = token_response.json()

        if 'error' in token_data:
            return Response({'error': token_data['error']}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_data.get('access_token')

        # Get user info
        user_info_url = 'https://graph.facebook.com/me'
        user_info_params = {
            'access_token': access_token,
            'fields': 'id,name,email'
        }
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()

        # Get or create social account
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=state)

        social_account, created = SocialAccount.objects.update_or_create(
            user=user,
            platform='facebook',
            platform_user_id=user_info['id'],
            defaults={
                'platform_username': user_info.get('name', ''),
                'access_token': access_token,
                'profile_data': user_info,
                'status': 'active',
                'last_sync_at': timezone.now()
            }
        )

        # Redirect to frontend with success
        return redirect(f"http://localhost:3000/channels?success=facebook")

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instagram_auth_url(request):
    """Get Instagram OAuth URL (uses Facebook)"""
    redirect_uri = settings.FACEBOOK_REDIRECT_URI.replace('facebook', 'instagram')
    scope = 'instagram_basic,instagram_manage_messages,instagram_manage_comments'

    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={settings.INSTAGRAM_APP_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&state={request.user.id}"
    )

    return Response({'auth_url': auth_url})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def linkedin_auth_url(request):
    """Get LinkedIn OAuth URL"""
    redirect_uri = settings.LINKEDIN_REDIRECT_URI
    scope = 'r_liteprofile,r_emailaddress,w_member_social'

    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code"
        f"&client_id={settings.LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&state={request.user.id}"
    )

    return Response({'auth_url': auth_url})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tiktok_auth_url(request):
    """Get TikTok OAuth URL"""
    redirect_uri = settings.TIKTOK_REDIRECT_URI
    scope = 'user.info.basic,video.list'

    auth_url = (
        f"https://www.tiktok.com/auth/authorize?"
        f"client_key={settings.TIKTOK_CLIENT_KEY}"
        f"&response_type=code"
        f"&scope={scope}"
        f"&redirect_uri={redirect_uri}"
        f"&state={request.user.id}"
    )

    return Response({'auth_url': auth_url})
