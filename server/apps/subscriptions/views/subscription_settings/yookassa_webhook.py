from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.utils import json
from apps.subscriptions.models import Payment, UserSubscription
from apps.subscriptions.services import YookassaService
from rest_framework.decorators import (
    api_view,
    permission_classes
)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def yookassa_webhook(request):
    """
    Вебхук для обработки уведомлений от ЮКассы
    """
    yookassa_service = YookassaService()
    signature = request.headers.get('Yookassa-Signature', '')

    if not yookassa_service.verify_webhook_signature(request.body, signature):
        return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = json.loads(request.body)
        event = data.get('event')
        payment_data = data.get('object', {})

        if event != 'payment.succeeded' and event != 'payment.canceled' and event != 'payment.waiting_for_capture':
            return Response({"status": "ignored"})

        payment_id = payment_data.get('id')
        payment_status = payment_data.get('status')

        payment = Payment.objects.get(yookassa_payment_id=payment_id)
        old_status = payment.status
        payment.status = payment_status

        if payment_status == 'succeeded' and old_status != 'succeeded':
            payment.paid_at = timezone.now()
            payment.save()

            subscription = payment.subscription
            subscription.is_active = True
            subscription.save()

            UserSubscription.objects.filter(
                user=payment.user,
                is_active=True
            ).exclude(id=subscription.id).update(is_active=False)

        elif payment_status in ['canceled', 'failed']:
            pass

        payment.save()

    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Webhook error: {e}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"status": "ok"})
