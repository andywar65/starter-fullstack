from datetime import datetime

import requests
from django.core.management.base import BaseCommand  # , CommandError
from django.db import transaction

from pages.models import Shotgun


class Command(BaseCommand):
    help = "Seed database with shotgun article data."

    @transaction.atomic
    def handle(self, *args, **options):
        #  TODO escape if shotgun exists
        self.stdout.write("Seeding database with shotgun articles...")

        target = "https://www.andywar.net/wp-json/wp/v2/posts?page="
        for i in range(1, 3):
            self.stdout.write("Page " + str(i))
            create_articles(target + str(i))

        self.stdout.write("Done.")


def create_articles(target):
    response = requests.get(target)
    wp_posts = response.json()
    for wp_post in wp_posts:
        date = datetime.fromisoformat(wp_post["date"])
        title = wp_post["title"]["rendered"]
        content = wp_post["content"]["rendered"]
        body = ""
        if "<p>" in content:
            body = content.split("<p>")[1].split("</p>")[0]
        link = ""
        if "data-orig-file" in content:
            link = content.split('data-orig-file="')[1].split('"')[0]
            body = body + link
        Shotgun.objects.create(title=title, date=date, body=body)
