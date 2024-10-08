import os
from django.core.management.base import BaseCommand
from django.conf import settings
from campuslife.models import Picture


class Command(BaseCommand):
    help = 'Import pictures from the media folder into the database'

    def handle(self, *args, **kwargs):
        pictures_dir = os.path.join(settings.MEDIA_ROOT, 'pictures')
        for filename in os.listdir(pictures_dir):
            if filename.endswith(('.jpg', '.png', '.jpeg')):  # Add more extensions if needed
                image_path = f'pictures/{filename}'
                # Check if this picture already exists in the database
                if not Picture.objects.filter(image=image_path).exists():
                    # Create a new Picture entry
                    picture = Picture(lodge_name=filename.split('.')[0], image=image_path)
                    picture.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully added {filename} to the database'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipping non-image file: {filename}'))
