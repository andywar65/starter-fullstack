# Generated by Django 4.0.3 on 2022-03-15 12:09

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_remove_homepage_carousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='logo',
            name='fb_image',
            field=filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name='Immagine'),
        ),
    ]
