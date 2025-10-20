from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'tiers', views.SubscriptionTierViewSet, basename='tier')
router.register(r'my-subscription', views.UserSubscriptionViewSet, basename='subscription')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/yookassa/', views.yookassa_webhook, name='yookassa-webhook'),
]
