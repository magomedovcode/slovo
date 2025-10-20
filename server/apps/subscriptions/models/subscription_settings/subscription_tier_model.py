from django.db import models


class SubscriptionTier(models.Model):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    level = models.IntegerField(
        unique=True,
        help_text="Уровень доступа (чем выше, тем больше возможностей)"
    )
    features = models.JSONField(
        default=list,
        help_text="Список доступных функций"
    )
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['level']

    def __str__(self):
        return f"{self.name} (Уровень {self.level})"
