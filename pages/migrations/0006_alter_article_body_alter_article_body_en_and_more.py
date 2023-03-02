# Generated by Django 4.0.3 on 2022-08-02 21:52

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0005_article_slug_en_article_slug_it"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="body",
            field=tinymce.models.HTMLField(null=True, verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="article",
            name="body_en",
            field=tinymce.models.HTMLField(null=True, verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="article",
            name="body_it",
            field=tinymce.models.HTMLField(null=True, verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(editable=False, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="slug_en",
            field=models.SlugField(editable=False, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="slug_it",
            field=models.SlugField(editable=False, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=tinymce.models.HTMLField(
                blank=True,
                help_text="Talk about this website",
                null=True,
                verbose_name="Text",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body_en",
            field=tinymce.models.HTMLField(
                blank=True,
                help_text="Talk about this website",
                null=True,
                verbose_name="Text",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body_it",
            field=tinymce.models.HTMLField(
                blank=True,
                help_text="Talk about this website",
                null=True,
                verbose_name="Text",
            ),
        ),
    ]