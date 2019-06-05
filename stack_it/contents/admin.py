"""Summary
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.translator import translator
from stack_it.models import (
    Menu,
    Page,
    Image,
    PageContent,
    TextPageContent,
    ImagePageContent,
    PagePageContent,
    ModelPageContent,
)
from mptt.admin import DraggableMPTTAdmin
from polymorphic.admin import StackedPolymorphicInline

from django.conf import settings
from stack_it.images.admin import ImageAdmin, build_image_thumb


# Register your models here.

if "modeltranslation" in settings.INSTALLED_APPS:
    from modeltranslation.admin import (
        TranslationBaseModelAdmin,
        TranslationStackedInline,
    )

    extra_parent_tabular_admin = (TranslationStackedInline,)
    extra_child_tabular_admin = (TranslationBaseModelAdmin,)
else:
    extra_admin = tuple()
    extra_parent_tabular_admin = tuple()
    extra_child_tabular_admin = tuple()


class ChildContentInline(*extra_child_tabular_admin, StackedPolymorphicInline.Child):

    """TextPageContent Inline admin
    See https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
    """

    def get_formset_child(self, request, obj=None, **kwargs):
        kwargs = self._get_form_or_formset(request, obj, **kwargs)
        return super(ChildContentInline, self).get_formset_child(request, obj, **kwargs)


class ParentContentInline(StackedPolymorphicInline, *extra_parent_tabular_admin):
    """TextPageContent Inline admin
    See https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
    """

    pass
