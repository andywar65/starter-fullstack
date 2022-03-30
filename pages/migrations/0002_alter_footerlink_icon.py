# Generated by Django 4.0.3 on 2022-03-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="footerlink",
            name="icon",
            field=models.CharField(
                choices=[
                    ("fa-external-link", "External link"),
                    ("fa-facebook", "Facebook"),
                    ("fa-instagram", "Instagram"),
                    ("fa-twitter", "Twitter"),
                    ("fa-linkedin", "LinkedIn"),
                    ("fa-github", "GitHub"),
                ],
                default="fa-external-link",
                max_length=50,
                verbose_name="Icon",
            ),
        ),
    ]
