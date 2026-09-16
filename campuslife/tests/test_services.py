from unittest.mock import patch

from django.test import TestCase, override_settings

from campuslife_services.payments import PaystackService
from campuslife_services.notifications import NotificationService


class PaystackServiceMockModeTests(TestCase):
    """With no PAYSTACK_SECRET_KEY set, the service must never hit the network
    and must still return the shape the calling views expect."""

    @patch.dict("os.environ", {}, clear=True)
    def test_mock_mode_is_active_without_a_secret_key(self):
        service = PaystackService()
        self.assertTrue(service.mock_mode)

    @patch.dict("os.environ", {"PAYSTACK_SECRET_KEY": "sk_test_dummy"})
    def test_real_mode_is_active_with_a_secret_key(self):
        service = PaystackService()
        self.assertFalse(service.mock_mode)

    @patch.dict("os.environ", {}, clear=True)
    def test_initialize_transaction_mock_response_shape(self):
        service = PaystackService()
        result = service.initialize_transaction(amount=5000, email="a@example.com", reference="CL-abc123")
        self.assertTrue(result["status"])
        self.assertIn("CL-abc123", result["data"]["authorization_url"])

    @patch.dict("os.environ", {}, clear=True)
    def test_verify_transaction_mock_response_shape(self):
        service = PaystackService()
        result = service.verify_transaction(reference="CL-abc123")
        self.assertEqual(result["data"]["status"], "success")

    def test_generate_reference_is_unique_and_prefixed(self):
        ref1 = PaystackService.generate_reference()
        ref2 = PaystackService.generate_reference()
        self.assertTrue(ref1.startswith("CL-"))
        self.assertNotEqual(ref1, ref2)


class NotificationServiceTests(TestCase):
    """Notifications must not attempt real SMTP without a configured password,
    and must not silently drop admin alerts when recipients ARE configured."""

    @patch.dict("os.environ", {}, clear=True)
    @patch("campuslife_services.notifications.EmailMessage")
    def test_send_is_suppressed_without_smtp_password(self, mock_email):
        NotificationService().send(subject="Test", body="Body", to=["someone@example.com"])
        mock_email.assert_not_called()

    @patch.dict("os.environ", {"EMAIL_HOST_PASSWORD": "dummy", "ADMIN_NOTIFICATION_EMAILS": "ops@example.com"})
    @patch("campuslife_services.notifications.EmailMessage")
    def test_notify_admins_sends_when_configured(self, mock_email):
        NotificationService().notify_admins(subject="Vacancy update", body="Body")
        mock_email.assert_called_once()
        _, kwargs = mock_email.call_args
        self.assertEqual(kwargs["to"], ["ops@example.com"])

    @patch.dict("os.environ", {"EMAIL_HOST_PASSWORD": "dummy"}, clear=True)
    @patch("campuslife_services.notifications.EmailMessage")
    def test_notify_admins_noop_without_recipients_configured(self, mock_email):
        NotificationService().notify_admins(subject="Vacancy update", body="Body")
        mock_email.assert_not_called()
