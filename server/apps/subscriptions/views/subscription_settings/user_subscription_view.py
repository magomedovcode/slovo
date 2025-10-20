from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.subscriptions.serializers.subscription_settings.user_subscription_serializer import UserSubscriptionSerializer
from apps.subscriptions.models import (
    UserSubscription,
    SubscriptionTier
)


class UserSubscriptionViewSet(viewsets.ReadOnlyModelViewSet):  # Только для чтения!
    """
    Просмотр подписки пользователя
    """
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)

    def get_object(self):
        subscription, created = UserSubscription.objects.get_or_create(
            user=self.request.user,
            defaults={
                'tier': SubscriptionTier.objects.filter(level=0).first(),
                'is_active': True
            }
        )
        return subscription
