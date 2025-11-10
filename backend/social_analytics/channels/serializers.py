from rest_framework import serializers
from .models import SocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = (
            'id', 'platform', 'platform_user_id', 'platform_username',
            'status', 'profile_data', 'created_at', 'updated_at', 'last_sync_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'last_sync_at')
