from modeltranslation.translator import register, TranslationOptions
from .models import Logo, FooterLink, HomePage, HomePageCarousel

@register(Logo)
class LogoTranslationOptions(TranslationOptions):
    fields = ('title', )
    #required_languages = ('it', 'en')

@register(FooterLink)
class FooterLinkTranslationOptions(TranslationOptions):
    fields = ('title', )
    #required_languages = ('it', 'en')

@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('title', 'intro', 'body', )
    #required_languages = ('it', 'en')

@register(HomePageCarousel)
class HomePageCarouselTranslationOptions(TranslationOptions):
    fields = ('description', )
    #required_languages = ('it', 'en')
