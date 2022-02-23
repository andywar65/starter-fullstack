from PIL import Image
from io import BytesIO

from django.db import models
from django.core.files import File
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.timezone import now

def modify_image_format(filename_ext):
    #TODO add all possible extensions
    conversion = {'JPG': 'JPEG',}
    ext = filename_ext.split('.')[-1].upper()
    return conversion[ext]

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
        #TODO save updated fields only?
        #make sure original image is loaded in db
        super(ImageData, self).save(*args, **kwargs)
        #get file data
        width = self.original.width
        height = self.original.height
        image = Image.open(self.original.path)
        filename_ext = self.original.name.replace('uploads/images/original/', '')
        #check title
        if not self.title:
            self.title = filename_ext.split('.')[0]
        #check versions
        if not self.thumbnail == self.original.name.replace('original', 'thumbnail'):
            if width>height:
                offset = (width-height)/2
                thumb = image.crop((offset,0,width-offset,height))
            elif height>width:
                offset = (height-width)/2
                thumb = image.crop((0,offset,width,height-offset))
            thumb.thumbnail((60,60))
            blob = BytesIO()
            thumb.save(blob, format=modify_image_format(filename_ext))
            self.thumbnail.save(filename_ext, File(blob), save=False)
        #save all the changes we've made
        super(ImageData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('-date', )
