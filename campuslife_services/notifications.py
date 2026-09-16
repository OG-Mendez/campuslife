import os

from django.conf import settings
from django.core.mail import EmailMessage


class NotificationService:
    def __init__(self):
        self.enabled = bool(os.getenv("EMAIL_HOST_PASSWORD"))
        raw = os.getenv("ADMIN_NOTIFICATION_EMAILS", "")
        self.admin_emails = [e.strip() for e in raw.split(",") if e.strip()]

    def send(self, *, subject, body, to):
        if not self.enabled:
            print(f"[NotificationService] Email suppressed (no SMTP configured): '{subject}' -> {to}")
            return
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=to,
            headers={"Content-Type": "text/plain"},
        ).send()

    def notify_admins(self, *, subject, body):
        if not self.admin_emails:
            print(f"[NotificationService] No ADMIN_NOTIFICATION_EMAILS configured — skipping: '{subject}'")
            return
        self.send(subject=subject, body=body, to=self.admin_emails)
