from modeltranslation.translator import register, TranslationOptions
from stack_it.models import Menu


@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ('name',)
