from modeltranslation.translator import register, TranslationOptions
from .models import Profile


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ("bio",)
    # required_languages = ('it', 'en')
