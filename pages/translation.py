from modeltranslation.translator import TranslationOptions, register

from .models import FooterLink, HomePage, HomePageCarousel, Logo


@register(Logo)
class LogoTranslationOptions(TranslationOptions):
    fields = ("title",)
    # required_languages = ('it', 'en')


@register(FooterLink)
class FooterLinkTranslationOptions(TranslationOptions):
    fields = ("title",)
    # required_languages = ('it', 'en')


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "intro",
        "body",
    )
    # required_languages = ('it', 'en')


@register(HomePageCarousel)
class HomePageCarouselTranslationOptions(TranslationOptions):
    fields = ("description",)
    # required_languages = ('it', 'en')
