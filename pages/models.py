from PIL import Image
from io import BytesIO

from django.db import models
from django.core.files import File
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.timezone import now

from filebrowser.fields import FileBrowseField

from .choices import ICONS

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
        upload_to = 'uploads/images/original/', null=True,
        help_text = _("""Landscape and at least 1600px wide if you want to use
            them in carousels"""), )
    thumbnail = models.ImageField(_('Thumbnail'),
        null=True, blank=True, upload_to = 'uploads/images/thumbnail/')
    popup = models.ImageField(_('Popup'),
        null=True, blank=True, upload_to = 'uploads/images/popup/')
    wide = models.ImageField(_('Wide'),
        null=True, blank=True, upload_to = 'uploads/images/wide/')
    date = models.DateTimeField(_('Date'), default = now, )

    def create_thumbnail(self, data):
        if data['width']>data['height']:
            offset = (data['width']-data['height'])/2
            thumb = data['image'].crop((offset,0,data['width']-offset,data['height']))
        elif data['height']>data['width']:
            offset = (data['height']-data['width'])/2
            thumb = data['image'].crop((0,offset,data['width'],data['height']-offset))
        else:
            thumb = data['image']
        thumb.thumbnail((64,64))
        blob = BytesIO()
        thumb.save(blob, format=modify_image_format(data['filename_ext']))
        self.thumbnail.save(data['filename_ext'], File(blob), save=False)

    def create_popup(self, data):
        if data['width']>data['height']:
            offset = (data['width']-data['height'])/2
            popup = data['image'].crop((offset,0,data['width']-offset,data['height']))
        elif data['height']>data['width']:
            offset = (data['height']-data['width'])/2
            popup = data['image'].crop((0,offset,data['width'],data['height']-offset))
        else:
            popup = data['image']
        popup.thumbnail((256,256))
        blob = BytesIO()
        popup.save(blob, format=modify_image_format(data['filename_ext']))
        self.popup.save(data['filename_ext'], File(blob), save=False)

    def create_wide(self, data):
        if data['height']>data['width']:
            return False
        if (data['width']/data['height']) > 2:
            w2 = data['height']*2
            offset = (data['width']-w2)/2
            wide = data['image'].crop((offset,0,data['width']-offset,data['height']))
        elif (data['width']/data['height']) < 2:
            h2 = data['width']*0.5
            offset = (data['height']-h2)/2
            wide = data['image'].crop((0,offset,data['width'],data['height']-offset))
        else:
            wide = data['image']
        wide.resize((1600,800))
        blob = BytesIO()
        wide.save(blob, format=modify_image_format(data['filename_ext']))
        self.wide.save(data['filename_ext'], File(blob), save=False)
        return True

    def save(self, *args, **kwargs):
        #make sure eventual original image is loaded in db
        super(ImageData, self).save(*args, **kwargs)
        #get file data
        if self.original:
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
            if not self.popup == self.original.name.replace('original', 'popup'):
                self.create_popup(data)
                changed = True
            if not self.wide == self.original.name.replace('original', 'wide'):
                wide_changed = self.create_wide(data)
                if wide_changed:
                    changed = True
            data['image'].close()
            #save all the changes we eventually made
            if changed:
                super(ImageData, self).save(*args, **kwargs)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return _('Image') + '-' + str(self.id)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('-date', )

class Logo(models.Model):

    title = models.CharField(_('Title'), max_length = 50,)
    image = models.ForeignKey(ImageData, on_delete = models.SET_NULL,
        related_name='logo_image', verbose_name = _('Image'), null=True )
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
        return self.title if self.title else _('Home Page - ') + str(self.id)

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
