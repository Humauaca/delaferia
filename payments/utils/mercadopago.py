import mercadopago
from datetime import datetime
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
dotenv_path = os.path.abspath(dotenv_path)

load_dotenv(dotenv_path)


class MercadoData:
    TEST_ACCESS_TOKEN = os.getenv('TEST_ACCESS_TOKEN')

    def __init__(self, **kwargs):
        self.total = kwargs.get('total')
        self.payment_method_id = kwargs.get('payment_method_id')
        self.payer_email = kwargs.get('email')
        self.card_data = {
            "card_number": kwargs.get('card_number'),
            "security_code": kwargs.get('security_code'),
            "expiration_month": kwargs.get('expiration_month'),
            "expiration_year": kwargs.get('expiration_year'),
            "cardholder": {
                "name": kwargs.get('name')
            }
        }
        self.installments = kwargs.get('installments', 1)
        self.unique_key = kwargs.get('unique_value')

    def __get_token_card(self):
        sdk = mercadopago.SDK(self.TEST_ACCESS_TOKEN) # type: ignore
        card_token_response = sdk.card_token().create(self.card_data)
        return card_token_response["response"]["id"]

    def get_data_to_save(self):
        sdk = mercadopago.SDK(self.TEST_ACCESS_TOKEN) # type: ignore

        # Idempotency header
        request_options = mercadopago.config.RequestOptions() # type: ignore
        request_options.custom_headers = {'x-idempotency-key': self.unique_key}

        # Payment payload
        payment_data = {
            "transaction_amount": self.total,
            "token": self.__get_token_card(),
            "description": "Payment description",
            "payment_method_id": self.payment_method_id,
            "installments": self.installments,
            "payer": {"email": self.payer_email}
        }

        # Make request
        result = sdk.payment().create(payment_data, request_options)
        payment = result["response"]

        # Serialize fields to save in model
        return {
            "external_payment_id": str(payment.get("id")),
            "status": payment.get("status"),
            "payment_method": payment.get("payment_method_id"),
            "amount": payment.get("transaction_amount"),
            "paid_at": self._parse_date(payment.get("date_approved")),
            "provider_data": payment
        }

    def _parse_date(self, date_str):
        if date_str:
            # Formato de fecha: '2025-07-21T12:11:04.186-04:00'
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return None




