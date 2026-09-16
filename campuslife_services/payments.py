import os
import uuid

from paystackapi.transaction import Transaction


class PaystackService:
    @staticmethod
    def generate_reference():
        return f"CL-{uuid.uuid4().hex[:16]}"

    def __init__(self):
        self.secret_key = os.getenv("PAYSTACK_SECRET_KEY")
        self.callback_url = os.getenv("PAYSTACK_CALLBACK_URL", "http://localhost:8000/payment/callback/")
        self.mock_mode = not bool(self.secret_key)

    def initialize_transaction(self, *, amount, email, reference):
        if self.mock_mode:
            return {
                "status": True,
                "data": {
                    "authorization_url": f"http://localhost:8000/mock-checkout/{reference}",
                    "reference": reference,
                },
            }
        return Transaction.initialize(
            key=self.secret_key,
            amount=amount,
            email=email,
            reference=reference,
            callback_url=self.callback_url,
        )

    def verify_transaction(self, *, reference):
        if self.mock_mode:
            return {
                "status": True,
                "data": {
                    "status": "success",
                    "amount": 40000,
                    "gateway_response": "Mocked verification (no PAYSTACK_SECRET_KEY set)",
                },
            }
        return Transaction.verify(key=self.secret_key, reference=reference)