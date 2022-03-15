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
