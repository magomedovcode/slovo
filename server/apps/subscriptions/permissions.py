from rest_framework import permissions
from .models import UserSubscription


class HasSubscriptionAccess(permissions.BasePermission):
    """
    Проверяет, имеет ли пользователь активную подписку необходимого уровня
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        try:
            subscription = request.user.subscription
            if not subscription.is_active:
                return False

            required_level = getattr(view, 'required_subscription_level', 0)
            if subscription.tier.level < required_level:
                return False

            required_feature = getattr(view, 'required_feature', None)
            if required_feature and not subscription.has_access(required_feature):
                return False

            return True

        except UserSubscription.DoesNotExist:
            return False
