# Generated by Django 4.0.3 on 2022-03-22 11:30

from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('link', models.URLField(verbose_name='Link')),
                ('icon', models.CharField(choices=[('fa-external-link', 'Link esterno'), ('fa-facebook', 'Facebook'), ('fa-instagram', 'Instagram'), ('fa-twitter', 'Twitter'), ('fa-linkedin', 'LinkedIn'), ('fa-github', 'GitHub')], default='fa-external-link', max_length=50, verbose_name='Icon')),
            ],
            options={
                'verbose_name': 'Footer link',
                'verbose_name_plural': 'Footer links',
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Appears on first image', max_length=50, null=True, verbose_name='Title')),
                ('title_it', models.CharField(blank=True, help_text='Appears on first image', max_length=50, null=True, verbose_name='Title')),
                ('title_en', models.CharField(blank=True, help_text='Appears on first image', max_length=50, null=True, verbose_name='Title')),
                ('intro', models.CharField(blank=True, help_text='Website in few words', max_length=100, null=True, verbose_name='Subtitle')),
                ('intro_it', models.CharField(blank=True, help_text='Website in few words', max_length=100, null=True, verbose_name='Subtitle')),
                ('intro_en', models.CharField(blank=True, help_text='Website in few words', max_length=100, null=True, verbose_name='Subtitle')),
                ('body', models.TextField(blank=True, help_text='Talk about this website', null=True, verbose_name='Text')),
                ('body_it', models.TextField(blank=True, help_text='Talk about this website', null=True, verbose_name='Text')),
                ('body_en', models.TextField(blank=True, help_text='Talk about this website', null=True, verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Home Page',
                'verbose_name_plural': 'Home Pages',
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('fb_image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Logo',
                'verbose_name_plural': 'Logo',
            },
        ),
        migrations.CreateModel(
            name='HomePageCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_image', filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Image')),
                ('description', models.CharField(blank=True, help_text='Will be used in captions', max_length=100, null=True, verbose_name='Description')),
                ('description_it', models.CharField(blank=True, help_text='Will be used in captions', max_length=100, null=True, verbose_name='Description')),
                ('description_en', models.CharField(blank=True, help_text='Will be used in captions', max_length=100, null=True, verbose_name='Description')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Position')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homepage_carousel', to='pages.homepage', verbose_name='Home Page')),
            ],
            options={
                'verbose_name': 'Home page carousel',
                'verbose_name_plural': 'Home page carousels',
                'ordering': ['position'],
            },
        ),
    ]
