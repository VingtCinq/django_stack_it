"""Summary
"""
from django.contrib import admin
from stack_it.models import(Menu,
                            Page,
                            Image,
                            PageContent,
                            TextPageContent,
                            ImagePageContent,
                            PagePageContent,
                            ModelPageContent,)
from mptt.admin import DraggableMPTTAdmin
from polymorphic.admin import (PolymorphicParentModelAdmin,
                               PolymorphicChildModelAdmin,
                               PolymorphicChildModelFilter,
                               PolymorphicInlineSupportMixin,
                               StackedPolymorphicInline)

from stack_it.images.admin import ImageAdmin
# Register your models here.


class PageContentInline(StackedPolymorphicInline):

    """
    Allow inline content modification

    Attributes:
        child_inlines (tuple): List inline admin classes
        model (class): Inline Base class
    """

    class PageContentInline(StackedPolymorphicInline.Child):

        """PageContent Inline admin
        See https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
        """

        model = PageContent

    class TextPageContentInline(StackedPolymorphicInline.Child):

        """TextPageContent Inline admin
        See https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
        """

        model = TextPageContent

    class ImagePageContentInline(StackedPolymorphicInline.Child):

        """ImagePageContent Inline admin
        See https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
        """

        model = ImagePageContent

    class PagePageContentInline(StackedPolymorphicInline.Child):

        """PagePageContent Inline admin
        See https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
        """

        model = PagePageContent

    class ModelPageContentInline(StackedPolymorphicInline.Child):

        """ModelPageContent Inline admin
        See https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
        """

        model = ModelPageContent

    model = PageContent
    child_inlines = (
        PageContentInline,
        TextPageContentInline,
        ImagePageContentInline,
        PagePageContentInline,
        ModelPageContentInline,
    )


class PageChildAdmin(PolymorphicInlineSupportMixin, PolymorphicChildModelAdmin):
    content_inlines = [PageContentInline, ]

    def __init__(self, *args, **kwargs):
        super(PageChildAdmin, self).__init__(*args, **kwargs)
        self.inlines += self.content_inlines


class PageAdmin(PolymorphicParentModelAdmin, DraggableMPTTAdmin):
    '''
    Admin View for Page
    Allows you to get custom "admin" within only one list

    See:
        https://django-polymorphic.readthedocs.io/en/stable/admin.html#example and 
        https://django-mptt.github.io/django-mptt/admin.html#mptt-admin-draggablempttadmin


    '''
    list_display = ('tree_actions', 'indented_title', 'verbose_name', 'status', 'slug', 'ref_full_path')
    list_display_links = (
        'indented_title',
    )
    list_filter = ('sites', 'status', PolymorphicChildModelFilter)
    child_models = ()
    readonly_fields = ('verbose_name','ref_full_path')


admin.site.register(Image, ImageAdmin)
