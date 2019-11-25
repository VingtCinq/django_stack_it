# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.apps import apps
from stack_it import urls as stack_it_urls
from stack_it import urls_i18n as stack_it_i18n_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(stack_it_urls)),
] + i18n_patterns(path("", include(stack_it_i18n_urls)))

