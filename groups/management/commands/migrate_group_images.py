# groups/management/commands/migrate_group_images.py
from django.core.management.base import BaseCommand
from groups.models import GroupImage
from cloudinary.uploader import upload
import os

class Command(BaseCommand):
    help = "Migrate all existing GroupImage images to Cloudinary"

    def handle(self, *args, **kwargs):
        images = GroupImage.objects.all()
        for img in images:
            # Skip if already migrated
            if img.image.url.startswith("https://res.cloudinary.com/"):
                self.stdout.write(f"Skipping already-migrated: {img.image}")
                continue

            # Skip if local file doesn't exist
            image_path = getattr(img.image, 'path', None)
            if not image_path or not os.path.isfile(image_path):
                self.stdout.write(f"Skipping missing file: {img.image}")
                continue

            self.stdout.write(f"Migrating: {img.image}")
            result = upload(image_path, folder="group_gallery")
            img.image = result['public_id']
            img.save()
            self.stdout.write(self.style.SUCCESS(f"Migrated to: {img.image}"))

        self.stdout.write(self.style.SUCCESS("All GroupImage images processed!"))