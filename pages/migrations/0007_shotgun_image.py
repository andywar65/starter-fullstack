# Generated by Django 4.0.3 on 2022-04-29 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0006_shotgun"),
    ]

    operations = [
        migrations.AddField(
            model_name="shotgun",
            name="image",
            field=models.ImageField(
                max_length=200,
                null=True,
                upload_to="uploads/images/shotgun/",
                verbose_name="Image",
            ),
        ),
    ]
