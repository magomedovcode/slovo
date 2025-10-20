from django.db import models
from django.conf import settings
from apps.subscriptions.models import SubscriptionTier


class UserSubscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    tier = models.ForeignKey(
        SubscriptionTier,
        on_delete=models.PROTECT
    )
    is_active = models.BooleanField(
        default=True
    )
    purchased_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-purchased_at']

    @property
    def has_access(self, feature=None):
        if not self.is_active:
            return False
        if feature:
            return feature in self.tier.features
        return True

    def can_upgrade_to(self, new_tier):
        return self.tier.level < new_tier.level

    def __str__(self):
        status = "активна" if self.is_active else "неактивна"
        return f"{self.user.username} - {self.tier.name} ({status})"
