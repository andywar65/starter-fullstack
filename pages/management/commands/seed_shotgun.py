from datetime import datetime
from io import BytesIO

import requests
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from pages.models import Shotgun, ShotgunImage


class Command(BaseCommand):
    help = "Seed database with shotgun article data."

    def handle(self, *args, **options):
        if Shotgun.objects.exists():
            raise CommandError(
                "This command cannot be run when any article exist, to guard "
                + "against accidental use on production."
            )
        self.stdout.write("Seeding database with shotgun articles...")

        list = [
            (370, 3),
            (371, 5),
            (372, 28),
            (373, 4),
            (374, 3),
        ]
        target = "https://www.rifondazionepodistica.it/wp-json/wp/v2/posts?page="
        for k in list:
            for i in range(1, k[1]):  # 1-72
                self.stdout.write("Category " + str(k[0]) + " - Page " + str(i))
                create_articles(target + str(i) + "&categories=" + str(k[0]))

        self.stdout.write("Done.")


def create_shotgun_image(shot, link):
    img = ShotgunImage.objects.create(description="", shot_id=shot.id)
    filename = link.split("/")[-1]
    r = requests.get(link)
    blob = BytesIO(r.content)
    img.image.save(filename, File(blob), save=True)


@transaction.atomic
def create_articles(target):
    r = requests.get(target)
    wp_posts = r.json()
    for wp_post in wp_posts:
        date = datetime.fromisoformat(wp_post["date"])
        title = wp_post["title"]["rendered"]
        content = wp_post["content"]["rendered"]
        body = ""
        list = content.split("<p>")
        for i in list[1:]:
            temp = i.split("</p>")[0]
            if "<img" not in temp and "<div" not in temp:
                body += temp + " "
        shot = Shotgun.objects.create(title=title, date=date, body=body)
        featured = wp_post["jetpack_featured_media_url"]
        if featured:
            create_shotgun_image(shot, featured)
        link = ""
        if "data-orig-file" in content:
            list = content.split('data-orig-file="')
            for i in list[1:]:
                link = i.split('"')[0]
                if "?fit" in link:
                    link = link.split("?fit")[0]
                if link:
                    create_shotgun_image(shot, link)
        elif "<figure" in content or "<img" in content:
            list = content.split('src="')
            for i in list[1:]:
                link = i.split('"')[0]
                if "?resize" in link:
                    link = link.split("?resize")[0]
                elif "?w=474" in link:
                    link = link.split("?w=474")[0]
                if link:
                    create_shotgun_image(shot, link)
