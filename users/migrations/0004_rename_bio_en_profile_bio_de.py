# Generated by Django 4.0.3 on 2022-04-14 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_profile_anonymize"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="bio_en",
            new_name="bio_de",
        ),
    ]
