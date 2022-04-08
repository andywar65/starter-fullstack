from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from pages.factories import ArticleFactory

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with article sample data."

    @transaction.atomic
    def handle(self, *args, **options):
        if settings.DEBUG is False:
            raise CommandError("This command cannot be run when DEBUG is False.")

        self.stdout.write("Seeding database with articles...")

        create_articles()

        self.stdout.write("Done.")


def create_articles():
    author = User.objects.first()
    if author:
        ArticleFactory.create_batch(9, author_id=author.uuid)
    else:
        ArticleFactory.create_batch(9)
