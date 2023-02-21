# Generated by Django 4.0.3 on 2022-04-05 11:43

import django.db.models.deletion
import django.utils.timezone
import filebrowser.fields
from django.conf import settings
from django.db import migrations, models

import pages.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pages", "0002_alter_footerlink_icon"),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(editable=False, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="The title of the article",
                        max_length=50,
                        verbose_name="Title",
                    ),
                ),
                (
                    "intro",
                    models.CharField(
                        default=pages.models.default_intro,
                        max_length=100,
                        verbose_name="Introduction",
                    ),
                ),
                ("body", models.TextField(null=True, verbose_name="Text")),
                (
                    "date",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Date"
                    ),
                ),
                ("last_updated", models.DateTimeField(editable=False, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
                "ordering": ("-date",),
            },
        ),
        migrations.CreateModel(
            name="ArticleCarousel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fb_image",
                    filebrowser.fields.FileBrowseField(
                        max_length=200, verbose_name="Image"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Will be used in captions",
                        max_length=100,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "position",
                    models.PositiveSmallIntegerField(
                        null=True, verbose_name="Position"
                    ),
                ),
                (
                    "home",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="article_carousel",
                        to="pages.article",
                        verbose_name="Article",
                    ),
                ),
            ],
            options={
                "verbose_name": "Article carousel",
                "verbose_name_plural": "Article carousels",
                "ordering": ["position"],
            },
        ),
    ]
