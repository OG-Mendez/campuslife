from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from campuslife.models import Agent, Order, Picture, Room, Wallet
from campuslife.views import payment, payment_callback


def _add_session(request):
    """RequestFactory requests don't go through SessionMiddleware automatically —
    payment() reads/writes request.session directly, so tests need a real one."""
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    return request


class PaymentCallbackTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="payer", password="pw12345", email="payer@example.com",
        )
        self.order = Order.objects.create(
            user=self.user, amount=400, email=self.user.email, reference="CL-test-ref", is_paid=False,
        )

    @patch.dict("os.environ", {}, clear=True)  # PaystackService mock mode: verify always reports success
    def test_successful_verification_marks_order_paid_and_credits_wallet(self):
        request = self.factory.get("/payment-callback/", {"reference": "CL-test-ref"})
        force_authenticate(request, user=self.user)

        response = payment_callback(request)

        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_paid)

        wallet = Wallet.objects.get(user=self.user)
        # Mock verify_transaction returns amount=40000 kobo -> 400 naira -> 400 // 400 = 1 point
        self.assertEqual(wallet.point, 1)

    @patch.dict("os.environ", {}, clear=True)
    def test_second_callback_for_same_reference_does_not_double_credit(self):
        request1 = self.factory.get("/payment-callback/", {"reference": "CL-test-ref"})
        force_authenticate(request1, user=self.user)
        payment_callback(request1)

        request2 = self.factory.get("/payment-callback/", {"reference": "CL-test-ref"})
        force_authenticate(request2, user=self.user)
        response2 = payment_callback(request2)

        self.assertEqual(response2.data.get("note"), "Already processed")
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(wallet.point, 1)  # only the first callback should have credited anything

    def test_missing_reference_returns_error_message(self):
        request = self.factory.get("/payment-callback/")
        force_authenticate(request, user=self.user)

        response = payment_callback(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.data)

    @patch.dict("os.environ", {}, clear=True)
    def test_unknown_reference_returns_400_not_a_server_error(self):
        request = self.factory.get("/payment-callback/", {"reference": "CL-does-not-exist"})
        force_authenticate(request, user=self.user)

        response = payment_callback(request)

        self.assertEqual(response.status_code, 400)

    @patch("campuslife_services.payments.PaystackService.verify_transaction")
    def test_failed_verification_does_not_mark_order_paid(self, mock_verify):
        mock_verify.return_value = {
            "status": True,
            "data": {"status": "failed", "gateway_response": "Insufficient funds"},
        }
        request = self.factory.get("/payment-callback/", {"reference": "CL-test-ref"})
        force_authenticate(request, user=self.user)

        response = payment_callback(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["reason"], "Insufficient funds")
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_paid)
        self.assertFalse(Wallet.objects.filter(user=self.user).exists())


class PaymentViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.student = User.objects.create_user(username="student", password="pw12345")
        self.agent_user = User.objects.create_user(username="agent_user", password="pw12345")
        self.agent = Agent.objects.create(
            user=self.agent_user, first_name="A", last_name="Gent",
            phone_number="08011111111", wallet=0,
        )
        self.picture = Picture.objects.create(lodge_name="Test Lodge", lodge_location="Nsukka")
        self.room = Room.objects.create(lodge=self.picture, room=self.agent, room_number=1, room_inspection=0)

    def _request(self, room_id):
        request = self.factory.post(f"/payment/?id={self.room.id}")
        force_authenticate(request, user=self.student)
        return _add_session(request)

    def test_unlocking_a_room_deducts_point_and_credits_agent(self):
        Wallet.objects.create(user=self.student, point=2)

        response = payment(self._request(self.room.id))

        self.assertEqual(response.status_code, 202)

        wallet = Wallet.objects.get(user=self.student)
        self.assertEqual(wallet.point, 1)

        self.agent.refresh_from_db()
        self.assertEqual(self.agent.wallet, 1)

        self.room.refresh_from_db()
        self.assertEqual(self.room.room_inspection, 1)

    def test_insufficient_points_returns_400_and_charges_nothing(self):
        Wallet.objects.create(user=self.student, point=0)

        response = payment(self._request(self.room.id))

        self.assertEqual(response.status_code, 400)
        self.agent.refresh_from_db()
        self.assertEqual(self.agent.wallet, 0)

    def test_missing_wallet_is_treated_as_zero_points_not_a_crash(self):
        # No Wallet row created at all for this user.
        response = payment(self._request(self.room.id))
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_room_returns_404(self):
        request = self.factory.post("/payment/?id=999999")
        force_authenticate(request, user=self.student)
        request = _add_session(request)

        response = payment(request)

        self.assertEqual(response.status_code, 404)

    def test_already_viewed_room_does_not_charge_again(self):
        Wallet.objects.create(user=self.student, point=2)
        request = self._request(self.room.id)
        request.session[f"viewed_room_{self.room.id}"] = True
        request.session.save()

        response = payment(request)

        self.assertEqual(response.status_code, 200)
        wallet = Wallet.objects.get(user=self.student)
        self.assertEqual(wallet.point, 2)  # untouched
