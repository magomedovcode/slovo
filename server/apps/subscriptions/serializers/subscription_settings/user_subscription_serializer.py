from rest_framework import serializers
from apps.subscriptions.serializers.subscription_settings.subscription_tier_serializer import SubscriptionTierSerializer
from apps.subscriptions.models import (
    SubscriptionTier,
    UserSubscription
)


class UserSubscriptionSerializer(serializers.ModelSerializer):
    tier = SubscriptionTierSerializer(read_only=True)
    tier_id = serializers.PrimaryKeyRelatedField(
        queryset=SubscriptionTier.objects.filter(is_active=True),
        source='tier',
        write_only=True
    )

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'user',
            'tier',
            'tier_id',
            'is_active',
            'purchased_at',
            'has_access'
        ]
        read_only_fields = [
            'user',
            'is_active',
            'purchased_at',
            'has_access'
        ]
