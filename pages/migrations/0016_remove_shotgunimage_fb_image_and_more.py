# Generated by Django 4.1.1 on 2024-03-15 19:09

import django.db.models.deletion
import filer.fields.image
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ("pages", "0015_shotgunimage_filer_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shotgunimage",
            name="fb_image",
        ),
        migrations.RemoveField(
            model_name="shotgunimage",
            name="image",
        ),
        migrations.AlterField(
            model_name="shotgunimage",
            name="filer_image",
            field=filer.fields.image.FilerImageField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="shotgun_filer_image",
                to=settings.FILER_IMAGE_MODEL,
            ),
        ),
    ]
