# Generated by Django 4.0.3 on 2022-03-11 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_alter_imagedata_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logo_image', to='pages.imagedata', verbose_name='Immagine')),
            ],
            options={
                'verbose_name': 'Logo',
                'verbose_name_plural': 'Logo',
            },
        ),
    ]
