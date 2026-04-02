from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from tinymce.models import HTMLField

from .choices import ICONS

User = get_user_model()


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
    icon = models.CharField(
        max_length=50, choices=ICONS, verbose_name=_("Icon"), default="fa-external-link"
    )

    class Meta:
        verbose_name = _("Footer link")
        verbose_name_plural = _("Footer links")


def default_intro():
    # following try/except for test to work
    try:
        current_site = Site.objects.get_current()
        return _("Another article by %(name)s!") % {"name": current_site.name}
    except Site.DoesNotExist:
        return _("Another article by this site!")


class Shotgun(models.Model):
    title = models.CharField(
        _("Title"), help_text=_("The title of the article"), max_length=100
    )
    body = HTMLField(_("Text"), null=True)
    date = models.DateField(
        _("Date"),
        default=now,
    )

    class Meta:
        verbose_name = _("Shotgun article")
        verbose_name_plural = _("Shotgun articles")
        ordering = [
            "-date",
        ]

    def get_card_width(self):
        for img in self.shotgun_image.all():
            if img.filer_image.width > img.filer_image.height:
                return "max-width: 960px"
        return "max-width: 480px"


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
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name = _("Shotgun image")
        verbose_name_plural = _("Shotgun images")
        ordering = [
            "position",
        ]
