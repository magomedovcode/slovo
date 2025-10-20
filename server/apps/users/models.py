from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.language.models import Language


class User(AbstractUser):
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    @property
    def has_active_subscription(self):
        if hasattr(self, 'subscription'):
            return self.subscription.is_valid
        return False

    REQUIRED_FIELDS = ['language']
