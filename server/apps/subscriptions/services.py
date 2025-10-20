import hashlib
import hmac
from yookassa import Payment, Configuration
from django.conf import settings


class YookassaService:
    def __init__(self):
        if not all([settings.YOOKASSA_ACCOUNT_ID, settings.YOOKASSA_SECRET_KEY]):
            raise ValueError("Yookassa credentials not configured")
        Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
        Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    @staticmethod
    def create_payment(amount, description, return_url, metadata=None):
        """Создание платежа в ЮКассе"""
        payment = Payment.create({
            "amount": {
                "value": f"{amount:.2f}",
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": description,
            "metadata": metadata or {}
        })

        return payment

    @staticmethod
    def verify_webhook_signature(request_body, signature_header):
        """Проверка подписи вебхука"""
        webhook_secret = getattr(settings, 'YOOKASSA_WEBHOOK_SECRET', '')

        if not webhook_secret or not signature_header:
            return False

        computed_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            request_body,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(computed_signature, signature_header)
