from rest_framework import serializers
from apps.subscriptions.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'subscription',
            'tier',
            'amount',
            'status',
            'created_at',
            'paid_at'
        ]
        read_only_fields = [
            'user',
            'subscription',
            'amount',
            'status',
            'created_at',
            'paid_at'
        ]
