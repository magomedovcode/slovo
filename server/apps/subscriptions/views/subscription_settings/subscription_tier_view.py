from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.subscriptions.models import SubscriptionTier
from apps.subscriptions.serializers.subscription_settings.subscription_tier_serializer import SubscriptionTierSerializer


class SubscriptionTierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр доступных тарифов подписки
    """
    queryset = SubscriptionTier.objects.filter(is_active=True)
    serializer_class = SubscriptionTierSerializer
    permission_classes = [AllowAny]
