from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from campuslife.models import (
    Picture, Interior, Rating, Review,
    Agent, Room, Wallet, Order, AgentEarning,
)

DEMO_IMAGE_DIR = Path(settings.BASE_DIR) / "campuslife" / "fixtures" / "demo_media"

SHARED_INTERIOR_IMAGE = "interior_placeholder.png"

DEMO_PASSWORD = "DemoPass123!"

FIXED_PAYOUT_DATE = timezone.make_aware(datetime(2026, 1, 15, 10, 0, 0))


class Command(BaseCommand):
    help = "Populate the database with deterministic demo data for local/reviewer use."

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        student, _ = User.objects.get_or_create(
            username="demo_student",
            defaults={"email": "demo_student@example.com"},
        )
        student.set_password(DEMO_PASSWORD)
        student.save()

        agent_user, _ = User.objects.get_or_create(
            username="demo_agent",
            defaults={"email": "demo_agent@example.com"},
        )
        agent_user.set_password(DEMO_PASSWORD)
        agent_user.save()

        agent, _ = Agent.objects.get_or_create(
            user=agent_user,
            defaults={
                "first_name": "Demo",
                "last_name": "Agent",
                "phone_number": "08000000000",
                "account_number": "0123456789",
                "bank_name": "Demo Bank",
                "wallet": 0,
            },
        )

        lodge_specs = [
            {
                "lodge_name": "Sunrise Hostel", "lodge_location": "Nsukka", "lodge_price": "150000",
                "available_vacancy": 3, "is_visible": True, "uploaded_by": agent_user,
                "lodge_image": "sunrise_hostel.png",
            },
            {
                "lodge_name": "Palm Court Lodge", "lodge_location": "Enugu", "lodge_price": "220000",
                "available_vacancy": 2, "is_visible": True, "uploaded_by": agent_user,
                "lodge_image": "palm_court_lodge.jpeg",
            },
            {
                "lodge_name": "Ivory Heights", "lodge_location": "Nsukka", "lodge_price": "180000",
                "available_vacancy": 0, "is_visible": True, "uploaded_by": agent_user,
                "lodge_image": "ivory_heights.jpeg",
            },
        ]

        pictures = []
        for spec in lodge_specs:
            lodge_image_filename = spec.pop("lodge_image")

            picture, created = Picture.objects.get_or_create(
                lodge_name=spec["lodge_name"],
                defaults=spec,
            )
            if created:
                self._attach_demo_image(picture, "image", lodge_image_filename)
            pictures.append(picture)

        for picture in pictures:
            interior, created = Interior.objects.get_or_create(
                picture=picture,
                defaults={},
            )
            if created:
                self._attach_demo_image(interior, "interior_image", SHARED_INTERIOR_IMAGE)

        Room.objects.get_or_create(
            lodge=pictures[0],
            room=agent,
            room_number=101,
            defaults={
                "room_type": "Self-contained",
                "room_floor": "1",
                "room_inspection": 0,
                "vacancy_indicator": True,
                "uploaded": True,
            },
        )

        rating, _ = Rating.objects.get_or_create(
            rated_by=student,
            picture_rating=pictures[0],
            defaults={"rating": 4},
        )
        Review.objects.get_or_create(
            rating=rating,
            created_by=student,
            defaults={"review": "Clean rooms, close to campus, would recommend."},
        )

        Wallet.objects.get_or_create(
            user=student,
            defaults={"point": 5},
        )
        Order.objects.get_or_create(
            reference="DEMO-REF-0001",
            defaults={
                "user": student,
                "amount": 5000,
                "email": student.email,
                "is_paid": True,
            },
        )

        AgentEarning.objects.get_or_create(
            agent=agent,
            payout_date=FIXED_PAYOUT_DATE,
            defaults={"payout_amount": 2000},
        )

        self.stdout.write(self.style.SUCCESS(
            f"Done.\n"
            f"  Student login -> username: demo_student / password: {DEMO_PASSWORD}\n"
            f"  Agent login   -> username: demo_agent   / password: {DEMO_PASSWORD}"
        ))

    def _attach_demo_image(self, instance, field_name, filename):
        src = DEMO_IMAGE_DIR / filename
        if not src.exists():
            self.stdout.write(self.style.WARNING(f"Missing demo image: {src}"))
            return
        with open(src, "rb") as f:
            getattr(instance, field_name).save(filename, File(f), save=True)
