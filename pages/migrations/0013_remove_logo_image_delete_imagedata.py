# Generated by Django 4.0.3 on 2022-03-15 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_logo_fb_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logo',
            name='image',
        ),
        migrations.DeleteModel(
            name='ImageData',
        ),
    ]
