import sys
from importlib import reload
from django.conf import settings

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from stack_it.seo.mixins import InternationalSlugMixin, SEOMixin
from stack_it.permissions.mixins import PermissionMixin
from stack_it.pages.managers import PageManager, TemplateManager, status_manager_factory
from stack_it.contents.abstracts import BaseContentMixin
from model_utils.fields import StatusField
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.db.models import Q
from polymorphic_tree.managers import PolymorphicMPTTModelManager


class Page(InternationalSlugMixin, PolymorphicMPTTModel, SEOMixin,PermissionMixin):
    """
    Page comes with features:
        Multilanguale Full Path denormalization
        Redirection management

    TODO:
        -Permissions management
        -Validation Pipeline & Versionning

    template_path is allowed to change template for one page inherited model.
    Your might want to have several "list" templates, and they should - mostly be compatible across themselves


    """

    SITE_ADMIN_FIELDSET = (
        _("Site"),
        {
            "fields": ("main_site", "sites"),
            "classes": ("collapse", "wide"),
            "description": _("Handle page's visibility on several websites"),
        },
    )
    PAGE_ADMIN_FIELDSET = (
        _("Page"),
        {
            "fields": ("title", "status", "key", "template_path", "slug"),
            "classes": ("wide",),
            "description": _("Handle page's status and data"),
        },
    )
    TREE_PARENT_FIELD = "parent"
    ENSURE_SLUG_UNICITY_BOOL = True
    HANDLE_REDIRECTION_BOOL = True
    SLUGIFY_FROM = "title"

    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS = ((DRAFT, _("Draft")), (PUBLISHED, _("Published")))
    template_path = models.CharField(
        verbose_name=_("Template Path"), default="", max_length=250
    )

    main_site = models.ForeignKey(
        Site,
        verbose_name=_("Main Site"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="pages_as_main_site",
        help_text=_(
            "In case the page is available on multiple websites, choose which one is to be considered as the main one"
        ),
    )
    sites = models.ManyToManyField(
        Site,
        verbose_name=_("Site"),
        help_text=_("This page will be available for each of those websites"),
    )
    parent = PolymorphicTreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    title = models.CharField(_("Title"), max_length=250)
    status = StatusField()
    verbose_name = models.CharField(_("Instance model verbose_name"), max_length=250)
    key = models.SlugField(
        _("Key for development"), max_length=250, blank=True, null=True
    )
    date_updated = models.DateTimeField(
        verbose_name=_("Last update date"), auto_now=True
    )

    objects = PageManager()
    base_manager = PolymorphicMPTTModelManager()
    published = status_manager_factory(PUBLISHED)()
    drafts = status_manager_factory(DRAFT)()

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.key is None:
            self.key = slugify(self.title)
        self.verbose_name = self._meta.verbose_name.title()
        super(Page, self).save(*args, **kwargs)
        try:
            reload(sys.modules[settings.ROOT_URLCONF])
        except KeyError:
            pass

    @property
    def values(self):
        if not hasattr(self, "_values"):
            if not hasattr(self, "content_values"):
                setattr(
                    self,
                    "content_values",
                    self.contents.filter(content_type=BaseContentMixin.VALUE),
                )
            setattr(
                self,
                "_values",
                dict([(instance.key, instance) for instance in self.content_values]),
            )
        return self._values

    @property
    def metas(self):
        if not hasattr(self, "_metas"):
            if not hasattr(self, "content_metas"):
                setattr(
                    self,
                    "content_metas",
                    self.contents.filter(content_type=BaseContentMixin.VALUE),
                )
            setattr(
                self,
                "_metas",
                dict([(instance.key, instance) for instance in self.content_metas]),
            )
        return self._metas

    def get_context_data(self, **kwargs):
        """Method planned to be overriden to allow extra context to be passed
        to view

        Returns:
            dict: A dict giving object's context
        """
        context = {}
        context.update(**kwargs)
        return context

    @property
    def url(self):
        return self.ref_full_path

    def get_absolute_url(self):
        return self.ref_full_path

    def get_cannonical_url(self):
        domain = ""

        if self.main_site_id is None and self.sites.count() == 1:
            domain = self.sites.first().domain
        if self.main_site_id is not None:
            domain = self.main_site.domain

            return domain + self.ref_full_path

    @classmethod
    def get_or_create(cls, title=""):
        slug = slugify(title)
        try:
            return cls.objects.rewrite(False).get(Q(title__iexact=title) | Q(slug=slug))
        except cls.DoesNotExist:
            return cls.objects.rewrite(False).create(
                title=title, **cls.build_international_kwargs_from_value("title", title)
            )


class Template(models.Model):
    """Model definition for Template."""

    name = models.CharField(_("Name"), max_length=250, blank=True, null=True)
    path = models.CharField(_("Path"), max_length=250)
    objects = TemplateManager()

    class Meta:
        """Meta definition for Template."""

        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    @property
    def values(self):
        if not hasattr(self, "_values"):
            if not hasattr(self, "content_values"):
                setattr(
                    self,
                    "content_values",
                    self.contents.filter(content_type=BaseContentMixin.VALUE),
                )
            setattr(
                self,
                "_values",
                dict([(instance.key, instance) for instance in self.content_values]),
            )
        return self._values

    @property
    def metas(self):
        if not hasattr(self, "_metas"):
            if not hasattr(self, "content_metas"):
                setattr(
                    self,
                    "content_metas",
                    self.contents.filter(content_type=BaseContentMixin.VALUE),
                )
            setattr(
                self,
                "_metas",
                dict([(instance.key, instance) for instance in self.content_metas]),
            )
        return self._metas

    def __str__(self):
        """Unicode representation of Template."""
        return self.name if self.name else self.path
