from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from stack_it.seo.mixins import InternationalSlugMixin, SEOMixin
from stack_it.pages.managers import PageManager, status_manager_factory
from stack_it.contents.abstracts import BaseContentMixin
from model_utils.fields import StatusField
from django.contrib.sites.models import Site


class Page(
        InternationalSlugMixin,
        SEOMixin,
        PolymorphicMPTTModel,
):
    """
    Page comes with features:
        Multilanguale Full Path denormalization
        Redirection management

    TODO:
        -SEO Management, see seo/mixins/SEOMixin
        -Validation Pipeline & Versionning

    template_path is allowed to change template for one page inherited model.
    Your might want to have several "list" templates, and they should - mostly be compatible across themselves


    """
    TREE_PARENT_FIELD = 'parent'
    ENSURE_SLUG_UNICITY_BOOL = True
    HANDLE_REDIRECTION_BOOL = True
    SLUGIFY_FROM = 'title'

    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published'))
    )
    template_path = models.CharField(verbose_name=_("Template Path"), default='', max_length=250)
    sites = models.ManyToManyField(Site, verbose_name=_("Site"))
    parent = PolymorphicTreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(_("Title"), max_length=150)
    status = StatusField()
    verbose_name = models.CharField(_("Instance model verbose_name"), max_length=50)
    objects = PageManager()
    published = status_manager_factory(PUBLISHED)()
    drafts = status_manager_factory(DRAFT)()

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.verbose_name = self._meta.verbose_name.title()
        super(Page, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)

        if not hasattr(self, 'content_values'):
            setattr(self, 'content_values', self.contents.filter(content_type=BaseContentMixin.VALUE))
        setattr(self, 'values', dict([(instance.key, instance) for instance in self.content_values]))

        if not hasattr(self, 'content_metas'):
            setattr(self, 'content_metas', self.contents.filter(content_type=BaseContentMixin.VALUE))
        setattr(self, 'metas', dict([(instance.key, instance) for instance in self.content_values]))

    def get_context_data(self, **kwargs):
        """Method planned to be overriden to allow extra context to be passed
        to view

        Returns:
            dict: A dict giving object's context
        """
        context = {}
        context.update(**kwargs)
        return context

    def get_absolute_url(self):
        return self.ref_full_path
