from rest_framework import serializers
from apps.subscriptions.models import SubscriptionTier


class SubscriptionTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionTier
        fields = [
            'id',
            'name',
            'description',
            'price',
            'level',
            'features',
            'is_active'
        ]
