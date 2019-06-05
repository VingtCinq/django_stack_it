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
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicInlineSupportMixin,
    StackedPolymorphicInline,
)

from django.conf import settings
from stack_it.images.admin import ImageAdmin, build_image_thumb
from stack_it.contents.admin import ChildContentInline, ParentContentInline

# Register your models here.
if "modeltranslation" in settings.INSTALLED_APPS:
    from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

    extra_admin = (TabbedDjangoJqueryTranslationAdmin,)
else:
    extra_admin = tuple()


class PageContentInline(ParentContentInline):

    """
    Allow inline content modification

    Attributes:
        child_inlines (tuple): List inline admin classes
        model (class): Inline Base class
    """

    class TextPageContentInline(ChildContentInline):

        """
        """

        model = TextPageContent

    class ImagePageContentInline(ChildContentInline):

        """Inline admin
        """

        model = ImagePageContent
        autocomplete_fields = ("image",)
        fields = ("image", "image_display", "size")
        readonly_fields = ("image_display",)
        image_display = build_image_thumb("image")
        image_display.short_description = _("Preview")

        # readonly_fields = ("key", "content_type", "ref_image", "ref_alt")

    class PagePageContentInline(ChildContentInline):

        """Inline admin
        """

        model = PagePageContent
        fields = ("value",)
        autocomplete_fields = ("value",)

    class ModelPageContentInline(ChildContentInline):

        """Inline admin
        """

        model = ModelPageContent

    model = PageContent
    child_inlines = (
        TextPageContentInline,
        ImagePageContentInline,
        PagePageContentInline,
        ModelPageContentInline,
    )

    def get_formset(self, request, obj=None, **kwargs):
        kwargs = self._get_form_or_formset(request, obj, **kwargs)
        print(self.trans_opts)
        exclude = self.replace_orig_field(kwargs.get("exclude")) or None
        exclude = self._exclude_original_fields(exclude)
        kwargs.update({"exclude": exclude})
        print(kwargs)
        return super(PageContentInline, self).get_formset(request, obj, **kwargs)


class PageChildAdmin(
    PolymorphicInlineSupportMixin, PolymorphicChildModelAdmin, *extra_admin
):
    content_inlines = [PageContentInline]

    def __init__(self, *args, **kwargs):
        super(PageChildAdmin, self).__init__(*args, **kwargs)
        inlines = getattr(self, "inlines")
        self.inlines = inlines + self.content_inlines


class PageAdmin(
    PolymorphicInlineSupportMixin,
    PolymorphicParentModelAdmin,
    DraggableMPTTAdmin,
    *extra_admin
):
    """
    Admin View for Page
    Allows you to get custom "admin" within only one list

    See:
        https://django-polymorphic.readthedocs.io/en/stable/admin.html#example and 
        https://django-mptt.github.io/django-mptt/admin.html#mptt-admin-draggablempttadmin


    """

    list_display = (
        "tree_actions",
        "indented_title",
        "verbose_name",
        "status",
        "slug",
        "ref_full_path",
    )
    inlines = [PageContentInline]
    list_display_links = ("indented_title",)
    list_filter = ("sites", "status", PolymorphicChildModelFilter)
    child_models = ()
    readonly_fields = ("verbose_name", "ref_full_path", "auto_slug")
    search_fields = ("title",)


admin.site.register(Image, ImageAdmin)
