from pathlib import Path

from django.conf import settings
from django.utils.text import slugify
from PIL import Image


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug exists.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    Thanks to djangosnippets.org!
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%d" % (origin_slug, numb)
        numb += 1
    return unique_slug


def check_wide_image(fb_image):
    """
    Checks if image is suitable for wide version. Performs 'version_generate',
    then controls dimensions. If small, pastes the image on a 1600x800 black
    background replacing original wide version. fb_image is a Fileobject.
    """
    img = fb_image.version_generate("wide")
    if img.width < 1600 or img.height < 800:
        path = Path(settings.MEDIA_ROOT).joinpath(fb_image.version_path("wide"))
        img = Image.open(path)
        back = Image.new(img.mode, (1600, 800))
        position = (
            int((back.width - img.width) / 2),
            int((back.height - img.height) / 2),
        )
        back.paste(img, position)
        back.save(path)


def check_wide_landscape_image(fb_image):
    """
    Checks if image is suitable for wide_landscape version. Performs 'version_generate',
    then controls dimensions. If small, pastes the image on a 1600x800 black
    background replacing original wide version. fb_image is a Fileobject.
    """
    img = fb_image.version_generate("wide_landscape")
    if img.width < 1600 or img.height < 800:
        path = Path(settings.MEDIA_ROOT).joinpath(
            fb_image.version_path("wide_landscape")
        )
        img = Image.open(path)
        back = Image.new(img.mode, (1600, 800))
        position = (
            int((back.width - img.width) / 2),
            int((back.height - img.height) / 2),
        )
        back.paste(img, position)
        back.save(path)
