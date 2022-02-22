from PIL import Image
from pathlib import Path

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.timezone import now

class ImageData(models.Model):

    title = models.CharField(_('Title'), max_length = 50,
        null=True, blank= True)
    description = models.CharField(_('Description'),
        help_text = _('Will be used in captions'),
        max_length = 100, null=True, blank=True)
    original = models.ImageField(_('Original image'),
        upload_to = 'uploads/images/original/')
    thumbnail = models.ImageField(_('Thumbnail'),
        null=True, blank=True, upload_to = 'uploads/images/thumbnail/')
    date = models.DateField(_('Date'), default = now, )

    def save(self, *args, **kwargs):
        #make sure original image is loaded in db
        super(ImageData, self).save(*args, **kwargs)
        filename_ext = self.original.name.replace('uploads/images/original/', '')
        filename = filename_ext.split('.')[0]
        if not self.title:
            self.title = filename
        if not self.thumbnail == 'uploads/images/thumbnail/' + filename_ext:
            self.original.open()
            image = Image.open(self.original)
            image.thumbnail((60,60), Image.ANTIALIAS)
            path = Path(settings.MEDIA_ROOT).joinpath('uploads/images/thumbnail/').joinpath(filename_ext)
            image.save( path, 'JPEG')
        #save all the changes we've made
        super(ImageData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('-date', )
