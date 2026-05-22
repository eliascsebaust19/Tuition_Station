import os
import json
import requests
from datetime import datetime, timedelta

class BkashConfig:
    APP_KEY = os.environ.get('BKASH_APP_KEY', '')
    APP_SECRET = os.environ.get('BKASH_APP_SECRET', '')
    USERNAME = os.environ.get('BKASH_USERNAME', '')
    PASSWORD = os.environ.get('BKASH_PASSWORD', '')
    BASE_URL = os.environ.get('BKASH_BASE_URL', 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized')
    MERCHANT_NUMBER = os.environ.get('BKASH_MERCHANT_NUMBER', '01XXXXXXXXX')
    CALLBACK_URL = os.environ.get('BKASH_CALLBACK_URL', 'http://localhost:5000/bkash/callback')

    @classmethod
    def is_configured(cls):
        return bool(cls.APP_KEY and cls.APP_SECRET and cls.USERNAME and cls.PASSWORD)


class BkashAPI:
    _token = None
    _token_expiry = None

    @classmethod
    def _headers(cls, token=None):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if token:
            headers['Authorization'] = token
            headers['X-APP-Key'] = BkashConfig.APP_KEY
        return headers

    @classmethod
    def grant_token(cls):
        if cls._token and cls._token_expiry and datetime.utcnow() < cls._token_expiry:
            return cls._token

        try:
            resp = requests.post(
                f'{BkashConfig.BASE_URL}/checkout/token/grant',
                json={'app_key': BkashConfig.APP_KEY, 'app_secret': BkashConfig.APP_SECRET},
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                timeout=30
            )
            data = resp.json()
            if 'id_token' in data:
                cls._token = data['id_token']
                cls._token_expiry = datetime.utcnow() + timedelta(hours=1)
                return cls._token
            raise Exception(data.get('errorMessage', 'Failed to grant token'))
        except Exception as e:
            raise Exception(f'bKash token error: {str(e)}')

    @classmethod
    def refresh_token(cls):
        cls._token = None
        cls._token_expiry = None
        return cls.grant_token()

    @classmethod
    def create_payment(cls, amount, invoice_number, payer_reference, callback_url=None):
        token = cls.grant_token()
        cb_url = callback_url or BkashConfig.CALLBACK_URL

        payload = {
            'mode': '0011',
            'payerReference': payer_reference,
            'callbackURL': cb_url,
            'amount': str(int(amount)),
            'currency': 'BDT',
            'intent': 'sale',
            'merchantInvoiceNumber': invoice_number,
        }

        resp = requests.post(
            f'{BkashConfig.BASE_URL}/checkout/payment/create',
            json=payload,
            headers=cls._headers(token),
            timeout=30
        )
        data = resp.json()

        if 'paymentID' in data and 'bkashURL' in data:
            return data
        raise Exception(data.get('errorMessage', 'Failed to create payment'))

    @classmethod
    def execute_payment(cls, payment_id):
        token = cls.grant_token()

        resp = requests.post(
            f'{BkashConfig.BASE_URL}/checkout/payment/execute',
            json={'paymentID': payment_id},
            headers=cls._headers(token),
            timeout=30
        )
        data = resp.json()

        if data.get('transactionStatus') == 'Completed':
            return data
        raise Exception(data.get('errorMessage', 'Payment execution failed'))

    @classmethod
    def query_payment(cls, payment_id):
        token = cls.grant_token()

        resp = requests.post(
            f'{BkashConfig.BASE_URL}/checkout/payment/status',
            json={'paymentID': payment_id},
            headers=cls._headers(token),
            timeout=30
        )
        return resp.json()
