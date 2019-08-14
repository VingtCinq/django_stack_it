from django.template import Library
from django.urls import translate_url as django_translate_url
from django.conf import settings
from django.contrib.sites.models import Site
from stack_it.models import Page
register = Library()


@register.simple_tag(takes_context=True)
def translate_url(context, page, lang_code):
    if type(page) == str:
        path = context.get('request').get_full_path()
        return django_translate_url(path, lang_code)
    else:
        return page.get_international_field_value("ref_full_path", lang_code)
