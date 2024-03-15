from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from filer.models import Image

from pages.models import ShotgunImage

User = get_user_model()


class Command(BaseCommand):
    help = "Get filebrowser images and create filer image."

    def handle(self, *args, **options):
        if Image.objects.exists():
            raise CommandError(
                "This command cannot be run if any Shotgun Image exists, "
                + "to prevent from accidental overwriting."
            )
        self.stdout.write("Generate filer images...")
        user = User.objects.filter(is_superuser=True).first()
        shots = ShotgunImage.objects.all()
        for shot in shots:
            generate_image(shot, user)

        self.stdout.write("Done.")


@transaction.atomic
def generate_image(shot, user):
    file_path = shot.fb_image.path_full
    filename = shot.fb_image.filename
    with open(file_path, "rb") as f:
        file_obj = File(f, name=filename)
        image = Image.objects.create(
            owner=user, original_filename=filename, file=file_obj
        )
    shot.filer_image = image
    shot.save()
