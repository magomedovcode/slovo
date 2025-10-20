from django.db import models
from django.conf import settings
from apps.subscriptions.models import (
    UserSubscription,
    SubscriptionTier
)


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('succeeded', 'Успешно'),
        ('canceled', 'Отменено'),
        ('failed', 'Ошибка'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE,
        null=True
    )
    tier = models.ForeignKey(
        SubscriptionTier,
        on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    yookassa_payment_id = models.CharField(
        max_length=100,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
