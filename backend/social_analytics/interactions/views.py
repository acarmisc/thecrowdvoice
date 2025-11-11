from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from social_analytics.channels.models import SocialAccount
from .models import Message
from .serializers import MessageSerializer
import requests
import json


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """View messages from all connected social accounts"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get messages from all user's social accounts
        user_accounts = SocialAccount.objects.filter(user=self.request.user)
        queryset = Message.objects.filter(social_account__in=user_accounts)

        # Filter by platform
        platform = self.request.query_params.get('platform')
        if platform:
            queryset = queryset.filter(social_account__platform=platform)

        # Filter by message type
        message_type = self.request.query_params.get('type')
        if message_type:
            queryset = queryset.filter(message_type=message_type)

        return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_messages(request, account_id):
    """Manually trigger message sync for a social account"""
    try:
        account = SocialAccount.objects.get(id=account_id, user=request.user)
    except SocialAccount.DoesNotExist:
        return Response({'error': 'Account non trovato'}, status=status.HTTP_404_NOT_FOUND)

    if account.platform == 'facebook':
        sync_facebook_messages(account)
    elif account.platform == 'instagram':
        sync_instagram_messages(account)
    # Add other platforms as needed

    account.last_sync_at = timezone.now()
    account.save()

    return Response({'message': 'Sincronizzazione avviata'})


def sync_facebook_messages(account):
    """Sync messages from Facebook"""
    # Get pages managed by the user
    url = f'https://graph.facebook.com/v18.0/me/accounts'
    params = {'access_token': account.access_token}

    response = requests.get(url, params=params)
    data = response.json()

    if 'error' in data:
        account.status = 'error'
        account.save()
        return

    pages = data.get('data', [])

    for page in pages:
        page_id = page['id']
        page_access_token = page['access_token']

        # Get conversations for this page
        conversations_url = f'https://graph.facebook.com/v18.0/{page_id}/conversations'
        conv_params = {
            'access_token': page_access_token,
            'fields': 'id,updated_time,messages{id,from,to,created_time,message}'
        }

        conv_response = requests.get(conversations_url, params=conv_params)
        conv_data = conv_response.json()

        conversations = conv_data.get('data', [])

        for conversation in conversations:
            conv_messages = conversation.get('messages', {}).get('data', [])

            for msg in conv_messages:
                # Store message in database
                Message.objects.update_or_create(
                    platform_message_id=msg['id'],
                    defaults={
                        'social_account': account,
                        'message_type': 'direct_message',
                        'platform_conversation_id': conversation['id'],
                        'sender_id': msg.get('from', {}).get('id', ''),
                        'sender_name': msg.get('from', {}).get('name', ''),
                        'text': msg.get('message', ''),
                        'raw_data': msg,
                        'received_at': msg.get('created_time'),
                    }
                )


def sync_instagram_messages(account):
    """Sync messages from Instagram"""
    # Similar to Facebook, using Instagram Graph API
    url = f'https://graph.facebook.com/v18.0/me/accounts'
    params = {'access_token': account.access_token}

    response = requests.get(url, params=params)
    data = response.json()

    # Implementation similar to Facebook
    pass
