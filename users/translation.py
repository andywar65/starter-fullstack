from modeltranslation.translator import TranslationOptions, register

from .models import Profile


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ("bio",)
    # required_languages = ('it', 'en')
