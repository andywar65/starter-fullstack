from django.db import models
from django.core.files import File
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from filebrowser.fields import FileBrowseField

from .choices import ICONS

class Logo(models.Model):

    title = models.CharField(_('Title'), max_length = 50,)
    fb_image = FileBrowseField(_("Image"), max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        directory='images/', null=True)

    class Meta:
        verbose_name = _('Logo')
        verbose_name_plural = _('Logo')

class FooterLink(models.Model):

    title = models.CharField(_('Title'), max_length = 50,)
    link = models.URLField(_('Link'), max_length = 200,)
    icon = models.CharField(max_length = 50, choices = ICONS,
        verbose_name = _('Icon'), default='fa-external-link')

    class Meta:
        verbose_name = _('Footer link')
        verbose_name_plural = _('Footer links')

class HomePage(models.Model):

    title = models.CharField(_('Title'),
        help_text=_("Appears on first image"),
        max_length = 50, null=True, blank=True)
    intro = models.CharField(_('Subtitle'), max_length = 100,
        null=True, blank=True, help_text = _('Website in few words'))
    body = models.TextField(_('Text'),
        null=True, blank=True, help_text = _('Talk about this website'))

    def __str__(self):
        if self.title:
            return self.title
        return _('Home Page - ') + str(self.id)

    class Meta:
        verbose_name = _('Home Page')
        verbose_name_plural = _('Home Pages')

class HomePageCarousel(models.Model):

    home = models.ForeignKey(HomePage, on_delete = models.CASCADE,
        related_name='homepage_carousel', verbose_name = _('Home Page') )
    fb_image = FileBrowseField(_("Image"), max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        directory='images/')
    description = models.CharField(_('Description'),
        help_text = _('Will be used in captions'),
        max_length = 100, null=True, blank=True)
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name = _('Home page carousel')
        verbose_name_plural = _('Home page carousels')
        ordering = ['position',]
