# Generated by Django 4.0.2 on 2022-02-12 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('first_name', 'last_name', 'username')},
        ),
    ]
