from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.subscriptions.serializers.subscription_settings.create_payment_serializer import CreatePaymentSerializer
from apps.subscriptions.serializers.subscription_settings.payment_serializer import PaymentSerializer
from apps.subscriptions.services import YookassaService
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.subscriptions.models import (
    Payment,
    SubscriptionTier,
    UserSubscription
)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Просмотр истории платежей
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tier = get_object_or_404(
            SubscriptionTier,
            id=serializer.validated_data['tier_id'],
            is_active=True
        )

        user_subscription, created = UserSubscription.objects.get_or_create(
            user=request.user,
            defaults={'tier': tier, 'is_active': False}
        )

        if not created:
            user_subscription.tier = tier
            user_subscription.is_active = False
            user_subscription.save()

        yookassa_service = YookassaService()
        return_url = request.build_absolute_uri('/subscription/success/')

        payment_data = yookassa_service.create_payment(
            amount=float(tier.price),
            description=f"Покупка подписки: {tier.name}",
            return_url=return_url,
            metadata={
                'user_id': request.user.id,
                'subscription_id': user_subscription.id,
                'tier_id': tier.id
            }
        )

        payment = Payment.objects.create(
            user=request.user,
            subscription=user_subscription,
            tier=tier,
            amount=tier.price,
            yookassa_payment_id=payment_data.id,
            status='pending'
        )

        return Response({
            'payment_id': payment.id,
            'confirmation_url': payment_data.confirmation.confirmation_url
        })
