from modeltranslation.translator import translator, TranslationOptions
from stack_it.models import (
    Page,
    PageContent,
    TextPageContent,
    ImagePageContent,
    PagePageContent,
    ModelPageContent,
    Template,
    TemplateContent,
    TextTemplateContent,
    ImageTemplateContent,
    PageTemplateContent,
)
from stack_it.seo.mixins import InternationalSlugMixin


class PageTranslation(TranslationOptions):
    fields = InternationalSlugMixin.TRANSLATION_FIELDS + [
        "slug",
        "title",
        "meta_description",
    ]


translator.register(Page, PageTranslation)


class TextPageContentTranslation(TranslationOptions):
    fields = ["value"]


translator.register(
    PageContent,
    type("PageContentTranslation", (TranslationOptions,), {"fields": tuple()}),
)
translator.register(TextPageContent, TextPageContentTranslation)
translator.register(
    ImagePageContent,
    type("ImagePageContentTranslation", (TranslationOptions,), {"fields": tuple()}),
)
translator.register(
    PagePageContent,
    type("PagePageContentTranslation", (TranslationOptions,), {"fields": tuple()}),
)
translator.register(
    ModelPageContent,
    type("ModelPageContentTranslation", (TranslationOptions,), {"fields": tuple()}),
)

translator.register(
    TemplateContent,
    type("TemplateContentTranslation", (TranslationOptions,), {"fields": tuple()}),
)
translator.register(TextTemplateContent, TextPageContentTranslation)
translator.register(
    ImageTemplateContent,
    type("ImageTemplateContentTranslation", (TranslationOptions,), {"fields": tuple()}),
)
translator.register(
    PageTemplateContent,
    type("PageTemplateContentTranslation", (TranslationOptions,), {"fields": tuple()}),
)
