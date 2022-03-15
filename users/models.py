import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject

class User(AbstractUser):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            p, created = Profile.objects.get_or_create(user_id = self.uuid)

    class Meta:
        ordering = ('first_name', 'last_name', 'username',)
        permissions = [
            ("can_not_change_profile", _("Immutable Profile")),
        ]

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False )
    temp_image = models.ImageField(_("Image"), max_length=200,
        null=True, blank=True, upload_to='uploads/images/users/')
    fb_image = FileBrowseField(_("Image"), max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, directory='images/users/')
    bio = models.TextField(_("Short bio"), null=True, blank=True)

    def get_full_name(self):
        if self.user.first_name and self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name
        else:
            return self.user.username
    get_full_name.short_description = _('Name')

    def get_short_name(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        #save and upload image
        super(Profile, self).save(*args, **kwargs)
        if self.temp_image:
            #image is saved on the front end, passed to fb_image and deleted
            self.fb_image=FileObject(str(self.temp_image))
            self.temp_image = None
            super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_message', verbose_name = _('User'), )
    subject = models.CharField(max_length = 200,
        verbose_name = _('Subject'), )
    body = models.TextField(verbose_name = _('Text'), )

    def __str__(self):
        return _('Message - %(id)d') % {'id': self.id}

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
