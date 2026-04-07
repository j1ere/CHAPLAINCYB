# theme/management/commands/migrate_to_cloudinary.py
from django.core.management.base import BaseCommand
from theme.models import Theme
from cloudinary.uploader import upload
import os

class Command(BaseCommand):
    help = "Migrate all existing Theme images to Cloudinary"

    def handle(self, *args, **kwargs):
        themes = Theme.objects.all()
        for theme in themes:
            image_path = getattr(theme.image, 'path', None)
            
            # Skip if the image is already a Cloudinary public_id
            if theme.image.url.startswith("https://res.cloudinary.com/"):
                self.stdout.write(f"Skipping already-migrated: {theme.image}")
                continue

            # Skip if local file doesn't exist
            if not image_path or not os.path.isfile(image_path):
                self.stdout.write(f"Skipping missing file: {theme.image}")
                continue

            self.stdout.write(f"Migrating: {theme.image}")
            result = upload(image_path, folder="themes")
            theme.image = result['public_id']
            theme.save()
            self.stdout.write(self.style.SUCCESS(f"Migrated to: {theme.image}"))

        self.stdout.write(self.style.SUCCESS("All images processed!"))