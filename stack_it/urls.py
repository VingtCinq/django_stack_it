from django.apps import apps
from django.urls import path, include,register_converter
from django.utils.translation import gettext_noop as _
from django.utils.functional import lazy
from stack_it.views import StackItView, key_redirect
from stack_it.utils.path import PagePathConverter
app_name = "stack_it"

register_converter(PagePathConverter, 'page')


urlpatterns = [
    path("", StackItView.as_view(), name="home"),
    path("<page:path>", StackItView.as_view(), name="page"),
    # path("<str:key>", StackItView.as_view(), name="page"),
]

