import uuid

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseField


class User(AbstractUser):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            p, created = Profile.objects.get_or_create(user_id=self.uuid)
            if created:
                content_type = ContentType.objects.get_for_model(Profile)
                permission = Permission.objects.get(
                    codename="change_profile",
                    content_type=content_type,
                )
                self.user_permissions.add(permission)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.username

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def get_avatar(self):
        if self.profile and self.profile.fb_image:
            thumb = self.profile.fb_image.version_generate("thumbnail")
            return thumb.url
        # attempts to retrieve avatar from social account
        try:
            s = SocialAccount.objects.get(user_id=self.uuid)
            return s.get_avatar_url()
        except SocialAccount.DoesNotExist:
            pass

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = (
            "first_name",
            "last_name",
            "username",
        )


class Profile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, editable=False
    )
    temp_image = models.ImageField(
        _("Image"),
        max_length=200,
        null=True,
        blank=True,
        upload_to="uploads/images/users/",
    )
    fb_image = FileBrowseField(
        _("Image"),
        max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True,
        blank=True,
        directory="images/users/",
    )
    bio = models.TextField(_("Short bio"), null=True, blank=True)
    anonymize = models.BooleanField(
        _("Anonymize"),
        default=False,
        help_text=_("Anonymize your account in public pages"),
    )

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        # save and upload image
        super(Profile, self).save(*args, **kwargs)
        if self.temp_image:
            # image is saved on the front end, passed to fb_image and deleted
            self.fb_image = FileObject(str(self.temp_image))
            self.temp_image = None
            super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


class UserMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_message",
        verbose_name=_("User"),
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject"),
    )
    body = models.TextField(
        verbose_name=_("Text"),
    )

    def __str__(self):
        return _("Message - %(id)d") % {"id": self.id}

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
