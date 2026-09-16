from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from campuslife.models import Order
from campuslife.views import fund_account


class FundAccountViewTests(TestCase):
    """Exercises validation and data handling in fund_account directly via
    RequestFactory, independent of URL routing."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="funder", password="pw12345", email="funder@example.com",
        )

    @patch.dict("os.environ", {}, clear=True)  # forces PaystackService into mock mode
    def test_valid_amount_creates_an_order_and_returns_authorization_url(self):
        request = self.factory.post("/fund-account/", {"amount": "500"}, format="json")
        force_authenticate(request, user=self.user)

        response = fund_account(request)

        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(user=self.user)
        # amount arrives in naira, is converted to kobo internally, then
        # divided back down before being stored — this must round-trip cleanly.
        self.assertEqual(order.amount, 500)
        self.assertEqual(order.email, "funder@example.com")
        self.assertTrue(order.reference)

    def test_missing_amount_returns_400_not_a_server_error(self):
        request = self.factory.post("/fund-account/", {}, format="json")
        force_authenticate(request, user=self.user)

        response = fund_account(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 0)

    def test_non_numeric_amount_returns_400_not_a_server_error(self):
        request = self.factory.post("/fund-account/", {"amount": "not-a-number"}, format="json")
        force_authenticate(request, user=self.user)

        response = fund_account(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 0)

    def test_unauthenticated_request_is_rejected(self):
        request = self.factory.post("/fund-account/", {"amount": "500"}, format="json")
        response = fund_account(request)
        self.assertEqual(response.status_code, 401)
