import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from tinymce.models import HTMLField


class Logo(models.Model):

    title = models.CharField(
        _("Title"),
        max_length=50,
    )
    image = FilerImageField(
        null=True, blank=True, related_name="logo_image", on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logo")


class FooterLink(models.Model):

    title = models.CharField(
        _("Title"),
        max_length=50,
    )
    link = models.URLField(
        _("Link"),
        max_length=200,
    )

    class Meta:
        verbose_name = _("Footer link")
        verbose_name_plural = _("Footer links")


def default_intro():
    text = """
<p>Introduction</p>
<details>
<summary>English text</summary>
<p>English text</p>
</details>
<details>
<summary>Testo in italiano</summary>
<p>Testo in italiano</p>
</details>"""
    return text


class Shotgun(models.Model):
    published = models.BooleanField(_("Published"), default=True)
    toot = models.BooleanField(_("Publish to Mastodon"), default=False)
    title = models.CharField(
        _("Title"), help_text=_("The title of the article"), max_length=100
    )
    slug = models.SlugField(_("Slug"), max_length=120, null=True, blank=True)
    body = HTMLField(_("Text"), default=default_intro)
    date = models.DateTimeField(
        _("Date"),
        default=now,
    )

    class Meta:
        verbose_name = _("Shotgun article")
        verbose_name_plural = _("Shotgun articles")
        ordering = [
            "-date",
        ]

    def get_absolute_url(self):
        return reverse("pages:shotgun_detail", args=[self.id, self.slug])

    def get_card_width(self):
        for img in self.shotgun_image.all():
            if img.filer_image.width > img.filer_image.height:
                return "max-width: 960px"
        return "max-width: 480px"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.toot and self.published:
            # Handle Mastodon publishing logic here
            domain = Site.objects.get_current().domain
            body = strip_tags(self.body.split("\n")[0])
            requests.post(
                settings.MASTODON_HOST,
                headers={"Authorization": f"Bearer {settings.MASTODON_TOKEN}"},
                data={"status": f"{body}\n https://{domain}{self.get_absolute_url()}"},
            )
            # Reset toot to False after handling Mastodon publishing
            self.toot = False
        super().save(*args, **kwargs)


class ShotgunImage(models.Model):
    shot = models.ForeignKey(
        Shotgun,
        on_delete=models.CASCADE,
        related_name="shotgun_image",
        verbose_name=_("Article"),
    )
    description = models.CharField(
        _("Description"),
        help_text=_("Used in captions"),
        max_length=200,
        null=True,
        blank=True,
    )
    filer_image = FilerImageField(
        null=True, related_name="shotgun_filer_image", on_delete=models.SET_NULL
    )
    position = models.PositiveSmallIntegerField(_("Position"), default=0)

    class Meta:
        verbose_name = _("Shotgun image")
        verbose_name_plural = _("Shotgun images")
        ordering = [
            "position",
        ]


class Story(models.Model):
    title = models.CharField(
        _("Title"), help_text=_("The title of the story"), max_length=100
    )
    slug = models.SlugField(_("Slug"), max_length=120, null=True, blank=True)
    description = models.CharField(
        _("Description"),
        help_text=_("Description of the story"),
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Shotgun story")
        verbose_name_plural = _("Shotgun stories")
        ordering = [
            "title",
        ]
