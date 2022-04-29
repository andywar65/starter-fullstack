from datetime import datetime
from io import BytesIO

import requests
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from pages.models import Shotgun


class Command(BaseCommand):
    help = "Seed database with shotgun article data."

    @transaction.atomic
    def handle(self, *args, **options):
        if Shotgun.objects.exists():
            raise CommandError(
                "This command cannot be run when any article exist, to guard "
                + "against accidental use on production."
            )
        self.stdout.write("Seeding database with shotgun articles...")

        target = "https://www.andywar.net/wp-json/wp/v2/posts?page="
        for i in range(1, 2):  # 55
            self.stdout.write("Page " + str(i))
            create_articles(target + str(i))

        self.stdout.write("Done.")


def create_articles(target):
    r = requests.get(target)
    wp_posts = r.json()
    for wp_post in wp_posts:
        date = datetime.fromisoformat(wp_post["date"])
        title = wp_post["title"]["rendered"]
        content = wp_post["content"]["rendered"]
        body = ""
        if "<p>" in content:
            body = content.split("<p>")[1].split("</p>")[0]
        shot = Shotgun.objects.create(title=title, date=date, body=body)
        if "data-orig-file" in content:
            link = content.split('data-orig-file="')[1].split('"')[0]
            filename = link.split("/")[-1]
            r = requests.get(link)
            blob = BytesIO(r.content)
            shot.image.save(filename, File(blob), save=True)
