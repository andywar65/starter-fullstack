# Generated by Django 4.0.3 on 2022-04-05 12:41

from django.db import migrations, models

import pages.models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0003_article_articlecarousel"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="body_en",
            field=models.TextField(null=True, verbose_name="Text"),
        ),
        migrations.AddField(
            model_name="article",
            name="body_it",
            field=models.TextField(null=True, verbose_name="Text"),
        ),
        migrations.AddField(
            model_name="article",
            name="intro_en",
            field=models.CharField(
                default=pages.models.default_intro,
                max_length=100,
                null=True,
                verbose_name="Introduction",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="intro_it",
            field=models.CharField(
                default=pages.models.default_intro,
                max_length=100,
                null=True,
                verbose_name="Introduction",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="title_en",
            field=models.CharField(
                help_text="The title of the article",
                max_length=50,
                null=True,
                verbose_name="Title",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="title_it",
            field=models.CharField(
                help_text="The title of the article",
                max_length=50,
                null=True,
                verbose_name="Title",
            ),
        ),
        migrations.AddField(
            model_name="articlecarousel",
            name="description_en",
            field=models.CharField(
                blank=True,
                help_text="Will be used in captions",
                max_length=100,
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AddField(
            model_name="articlecarousel",
            name="description_it",
            field=models.CharField(
                blank=True,
                help_text="Will be used in captions",
                max_length=100,
                null=True,
                verbose_name="Description",
            ),
        ),
    ]
