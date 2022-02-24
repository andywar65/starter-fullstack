import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from pages.models import ImageData

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
    avatar = models.ForeignKey(ImageData, on_delete = models.SET_NULL,
        related_name='profile_avatar', verbose_name = _('Avatar'), null=True,
        blank=True)
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

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
