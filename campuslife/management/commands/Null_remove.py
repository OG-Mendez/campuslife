# your_app/management/commands/populate_caretaker_number.py
from django.core.management.base import BaseCommand
from campuslife.models import Picture


class Command(BaseCommand):
    help = 'Populate caretaker_number with a default integer value where it is null'

    def handle(self, *args, **kwargs):
        default_value = 0  # Change to any integer you prefer
        updated_count = Picture.objects.filter(caretaker_number__isnull=True).update(caretaker_number=default_value)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} records'))

