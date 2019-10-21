from django.apps import apps
from django.urls import path, include
from django.utils.translation import gettext_noop as _
from django.utils.functional import lazy
from stack_it.views import StackItView, key_redirect

app_name = "stack_it"


urlpatterns = [
    path("", StackItView.as_view()),
    path("<path:path>", StackItView.as_view()),
    path("<str:key>", StackItView.as_view(), name="page"),
]

