from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from filebrowser.fields import FileBrowseField

from project.utils import check_tall_image, check_wide_image, generate_unique_slug

from .choices import ICONS

User = get_user_model()


class Logo(models.Model):

    title = models.CharField(
        _("Title"),
        max_length=50,
    )
    fb_image = FileBrowseField(
        _("Image"),
        max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        directory="images/",
        null=True,
    )

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logo")


class FooterLink(models.Model):

    title = models.CharField(
        _("Title"),
        max_length=50,
    )
    link = models.URLField(
        _("Link"),
        max_length=200,
    )
    icon = models.CharField(
        max_length=50, choices=ICONS, verbose_name=_("Icon"), default="fa-external-link"
    )

    class Meta:
        verbose_name = _("Footer link")
        verbose_name_plural = _("Footer links")


class HomePage(models.Model):

    title = models.CharField(
        _("Title"),
        help_text=_("Appears on first image"),
        max_length=50,
        null=True,
        blank=True,
    )
    intro = models.CharField(
        _("Subtitle"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Website in few words"),
    )
    body = models.TextField(
        _("Text"), null=True, blank=True, help_text=_("Talk about this website")
    )

    def __str__(self):
        if self.title:
            return self.title
        return _("Home Page - ") + str(self.id)

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")


class HomePageCarousel(models.Model):

    home = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="homepage_carousel",
        verbose_name=_("Home Page"),
    )
    fb_image = FileBrowseField(
        _("Image"),
        max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        directory="images/",
    )
    description = models.CharField(
        _("Description"),
        help_text=_("Will be used in captions"),
        max_length=100,
        null=True,
        blank=True,
    )
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name = _("Home page carousel")
        verbose_name_plural = _("Home page carousels")
        ordering = [
            "position",
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        check_wide_image(self.fb_image)


def default_intro():
    # following try/except for test to work
    try:
        current_site = Site.objects.get_current()
        return _("Another article by %(name)s!") % {"name": current_site.name}
    except Site.DoesNotExist:
        return _("Another article by this site!")


class Article(models.Model):
    slug = models.SlugField(max_length=50, editable=False, null=True)
    title = models.CharField(
        _("Title"), help_text=_("The title of the article"), max_length=50
    )
    intro = models.CharField(_("Introduction"), default=default_intro, max_length=100)
    body = models.TextField(_("Text"), null=True)
    date = models.DateField(
        _("Date"),
        default=now,
    )
    last_updated = models.DateTimeField(editable=False, null=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Author")
    )

    def get_path(self):
        return reverse(
            "pages:article_detail",
            kwargs={
                "year": self.date.year,
                "month": self.date.month,
                "day": self.date.day,
                "slug": self.slug,
            },
        )

    def get_previous(self):
        try:
            return self.get_previous_by_date()
        except Article.DoesNotExist:
            return

    def get_next(self):
        try:
            return self.get_next_by_date()
        except Article.DoesNotExist:
            return

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Article, self.title)
        self.last_updated = now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-date",)


class ArticleCarousel(models.Model):

    home = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="article_carousel",
        verbose_name=_("Article"),
    )
    fb_image = FileBrowseField(
        _("Image"),
        max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        directory="images/",
    )
    description = models.CharField(
        _("Description"),
        help_text=_("Will be used in captions"),
        max_length=100,
        null=True,
        blank=True,
    )
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name = _("Article carousel")
        verbose_name_plural = _("Article carousels")
        ordering = [
            "position",
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        check_wide_image(self.fb_image)


class Shotgun(models.Model):
    title = models.CharField(
        _("Title"), help_text=_("The title of the article"), max_length=50
    )
    body = models.TextField(_("Text"), null=True)
    date = models.DateField(
        _("Date"),
        default=now,
    )
    fb_image = FileBrowseField(
        _("Image"),
        max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        directory="images/shotgun/",
        null=True,
    )

    class Meta:
        verbose_name = _("Shotgun article")
        verbose_name_plural = _("Shotgun articles")
        ordering = [
            "-date",
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        check_tall_image(self.fb_image)
