from datetime import datetime

import requests
from django.core.management.base import BaseCommand  # , CommandError
from django.db import transaction

from pages.models import Shotgun


class Command(BaseCommand):
    help = "Seed database with shotgun article data."

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("Seeding database with shotgun articles...")

        create_articles()

        self.stdout.write("Done.")


def create_articles():
    target = "https://www.andywar.net/wp-json/wp/v2/posts"
    response = requests.get(target)
    wp_posts = response.json()
    for wp_post in wp_posts:
        date = datetime.fromisoformat(wp_post["date"])
        title = wp_post["title"]["rendered"]
        Shotgun.objects.create(title=title, date=date)
