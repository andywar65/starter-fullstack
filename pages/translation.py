from modeltranslation.translator import TranslationOptions, register

from .models import FooterLink, Logo


@register(Logo)
class LogoTranslationOptions(TranslationOptions):
    fields = ("title",)
    # required_languages = ('it', 'en')


@register(FooterLink)
class FooterLinkTranslationOptions(TranslationOptions):
    fields = ("title",)
    # required_languages = ('it', 'en')
