from PIL import Image
from io import BytesIO

from django.db import models
from django.core.files import File
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.timezone import now

def modify_image_format(filename_ext):
    """We get the extention directly from original file, but sometimes
    in PIL.Image.save(file, format='XXX') resulting format string is not
    recognized. Use conversion dict to modify string."""
    conversion = {'JPG': 'JPEG',}
    ext = filename_ext.split('.')[-1].upper()
    if conversion[ext]:
        return conversion[ext]
    return ext

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

    def create_thumbnail(self, data):
        if data['width']>data['height']:
            offset = (data['width']-data['height'])/2
            thumb = data['image'].crop((offset,0,data['width']-offset,data['height']))
        elif data['height']>data['width']:
            offset = (data['height']-data['width'])/2
            thumb = data['image'].crop((0,offset,data['width'],data['height']-offset))
        thumb.thumbnail((64,64))
        blob = BytesIO()
        thumb.save(blob, format=modify_image_format(data['filename_ext']))
        self.thumbnail.save(data['filename_ext'], File(blob), save=False)

    def save(self, *args, **kwargs):
        #make sure original image is loaded in db
        super(ImageData, self).save(*args, **kwargs)
        #get file data
        data = {
            'width' : self.original.width,
            'height' : self.original.height,
            'image' : Image.open(self.original.path),
            'filename_ext' : self.original.name.replace('uploads/images/original/', ''),
        }
        changed = False
        #check title
        if not self.title:
            self.title = data['filename_ext'].split('.')[0]
            changed = True
        #check versions
        if not self.thumbnail == self.original.name.replace('original', 'thumbnail'):
            self.create_thumbnail(data)
            changed = True
        data['image'].close()
        #save all the changes we eventually made
        if changed:
            super(ImageData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('-date', )
