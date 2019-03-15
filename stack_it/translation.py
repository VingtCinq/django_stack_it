from modeltranslation.translator import translator, TranslationOptions
from stack_it.models import Page
from stack_it.seo.mixins import InternationalSlugMixin


class PageTranslation(TranslationOptions):
    fields = InternationalSlugMixin.TRANSLATION_FIELDS + [
        'slug',
        'title',
    ]


translator.register(Page, PageTranslation)
