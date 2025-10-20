from rest_framework import serializers
from apps.subscriptions.models import SubscriptionTier


class CreatePaymentSerializer(serializers.Serializer):
    tier_id = serializers.IntegerField()

    def validate_tier_id(self, value):
        try:
            tier = SubscriptionTier.objects.get(id=value, is_active=True)

            user_subscription = getattr(self.context['request'].user, 'subscription', None)
            if user_subscription and user_subscription.tier.level > tier.level:
                raise serializers.ValidationError("Нельзя понизить уровень подписки")

            return value
        except SubscriptionTier.DoesNotExist:
            raise serializers.ValidationError("Тариф не найден или неактивен")
