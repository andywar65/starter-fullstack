from django.db import models
from django.utils.translation import gettext as _
from django.utils.timezone import now

class ImageData(models.Model):

    title = models.CharField(_('Title'), max_length = 50, null=True, )
    description = models.CharField(_('Description'),
        help_text = _('Will be used in captions'),
        max_length = 100, null=True, blank=True)
    original = models.ImageField(_('Original image'),
        upload_to = 'uploads/images/original/')
    thumbnail = models.ImageField(_('Thumbnail'),
        null=True, blank=True)
    date = models.DateField(_('Date'), default = now, )

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('-date', )
