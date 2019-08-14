from django.db import models, transaction
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.validators import ValidationError
from django.core.exceptions import ImproperlyConfigured
from stack_it.utils.models.mixins import InternationalMixin
from stack_it.seo.helpers import handle_redirection
from django.contrib.redirects.models import Redirect


class SEOMixin(models.Model):
    """
    Simple page to handle SEO specific fields & problematic
    """

    SEO_ADMIN_FIELDSET = (
        (
            _("Meta"),
            {
                "fields": (
                    (
                        "meta_title",
                        "meta_description",
                        "meta_image",
                        "meta_image_display",
                        "priority",
                    ),
                ),
                "classes": ("collapse", "wide"),
                "description": _("Handle page's Meta"),
            },
        ),
        (
            _("Twitter Meta"),
            {
                "fields": (
                    ("tw_title", "tw_description", "tw_image", "tw_image_display"),
                ),
                "classes": ("collapse", "wide"),
                "description": _("Handle page's Twitter Meta"),
            },
        ),
        (
            _("Open Graph Meta"),
            {
                "fields": (
                    ("og_title", "og_description", "og_image", "og_image_display"),
                ),
                "classes": ("collapse", "wide"),
                "description": _("Handle page's OpenGraph (Facebooks) Meta"),
            },
        ),
    )

    ALWAYS = "always"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    NEVER = "never"

    FREQUENCIES = (
        (ALWAYS, _("always")),
        (HOURLY, _("hourly")),
        (DAILY, _("daily")),
        (WEEKLY, _("weekly")),
        (MONTHLY, _("monthly")),
        (YEARLY, _("yearly")),
        (NEVER, _("never")),
    )
    meta_description = models.CharField(
        _("Meta Description"),
        max_length=250,
        default="",
        help_text=_("keep this under 160 characters for best optimisation"),
    )
    meta_title = models.TextField(
        _("Meta Title"),
        default="",
        help_text=_("keep this under 60 characters for best optimisation"),
    )
    meta_image = models.ForeignKey(
        "stack_it.Image",
        on_delete=models.CASCADE,
        verbose_name=_("Meta Image"),
        blank=True,
        null=True,
        related_name="meta_images",
    )
    tw_title = models.CharField(
        _("Twitter Title"),
        help_text=_("Keep this under 70 characters for best optimisation"),
        max_length=100,
        blank=True,
    )
    tw_description = models.TextField(
        _("Twitter Description"),
        help_text=_("Twitter description less than 200 characters"),
        blank=True,
    )
    tw_image = models.ForeignKey(
        "stack_it.Image",
        on_delete=models.CASCADE,
        verbose_name=_("Twitter Image"),
        help_text=_("must be at least 120x120px"),
        blank=True,
        null=True,
        related_name="tw_images",
    )
    ## Facebook
    og_title = models.CharField(
        _("Facebook Title"),
        help_text=_("Keep it under 55 characters for best optimisation"),
        max_length=100,
        blank=True,
    )
    og_description = models.TextField(
        _("Facebook Description"),
        help_text=_("Facebook description less than 300 characters"),
        blank=True,
    )
    og_image = models.ForeignKey(
        "stack_it.Image",
        on_delete=models.CASCADE,
        verbose_name=_("Facebook Image"),
        help_text=_("must be at least 1200x630px"),
        blank=True,
        null=True,
        related_name="od_images",
    )

    priority = models.FloatField(_("Page priority for indexation"), default=0.5)
    changefreq = models.CharField(
        _("Page change frequency"), max_length=50, choices=FREQUENCIES, default=MONTHLY
    )

    class Meta:
        abstract = True

    def _is_valid_length(self, attr, length):
        value = len(getattr(self, attr))
        return value <= length and value >= length / 2

    def get_meta_tags(self, include_site_meta=True):
        if include_site_meta:
            meta = SiteMeta.get_meta_tags()
        else:
            meta = {}
        for field in [
            "meta_title",
            "meta_description",
            "tw_title",
            "tw_description",
            "og_title",
            "og_description",
        ]:
            meta[field] = getattr(self, field, "")
        for field in ["og_image", "tw_image"]:
            if getattr(self, field):
                meta[field] = getattr(getattr(self, field), "url")
            else:
                meta[field] = ""
        meta["has_tw"] = self.has_tw
        meta["has_og"] = self.has_og
        return meta

    @property
    def has_tw(self):
        return all(getattr(self, field) for field in self.TW_REQUIRED_FIELDS)

    @property
    def has_og(self):
        return all(getattr(self, field) for field in self.OG_REQUIRED_FIELDS)

    @property
    def overall_score(self):
        score = []
        for key, value in self.VALID_LENGTH.items():
            score.append(int(self._is_valid_length(key, value)))
        return int(mean(score) * 100)

    @property
    def overall_score_str(self):
        return f"{str(self.overall_score)}%"


class InternationalSlugMixin(InternationalMixin):

    """Summary

    Attributes:
        ENSURE_SLUG_UNICITY_BOOL (bool): Make sure your slug is unique accross Inherited models.
            If set to False, slug unicity will not be checked
        HANDLE_REDIRECTION_BOOL (bool): When a change is made to the instance slug,
            a redirection will be automatically created.
            If set to False, no redirections will be created for the model
        SLUGIFY_FROM (str): Gives the field name to slugify from
        TREE_PARENT_FIELD (str): Gives the name of the "parent" attribute.
            The parent attribute instances should defined at least a "ref_full_path" attribute,
            while instance should implement a "get_children" method
        auto_slug (BooleanField): Defines if the slug is updated when attribute defined by
            class's SLUGIFY_FROM is changed
        ref_full_path (SlugField): A denormalization field, to keep the instance "full path"
            slug (SlugField): Instances stand-alone slug
    """

    TREE_PARENT_FIELD = None
    ENSURE_SLUG_UNICITY_BOOL = False
    HANDLE_REDIRECTION_BOOL = False
    SLUGIFY_FROM = None
    TRANSLATION_FIELDS = ["slug", "auto_slug", "ref_full_path"]
    slug = models.SlugField(_("Slug"), blank=True, max_length=500)
    auto_slug = models.BooleanField(
        _("Auto Slug"),
        help_text=_(
            "When set, your slug will automatically be updated from field define in class's SLUGIFY_FROM"
        ),
        default=True,
    )
    ref_full_path = models.SlugField(
        _("Denormalized full path"), editable=False, max_length=500
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Usual Django "save" override.
        It allows:
        -auto slugification when instance's `auto_slug`is set to True
        -full path i18n denormalization

        Args:
            *args: Not different from django's native method
            **kwargs: Not different from django's native method

        Returns:
            None
        """
        self.clean()
        super(InternationalSlugMixin, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        created = self.pk is None
        self.slugify(created)
        self.denormalize_full_path(created=created, save=False)
        if self.ENSURE_SLUG_UNICITY_BOOL:
            self.ensure_slug_unicity()
        super(InternationalSlugMixin, self).clean(*args, **kwargs)

    @property
    def _parent(self):
        """
        Allows to retrieve "parent" - according to a transversal tree lexic.

        Returns:
            The child's class attribute named after TREE_PARENT_FIELD in class's definition

        Raises:
            ImproperlyConfigured: When TREE_PARENT_FIELD if not relevant faced to the real class
        """
        field = hasattr(self, self.TREE_PARENT_FIELD)
        if field:
            return getattr(self, self.TREE_PARENT_FIELD)
        else:
            raise ImproperlyConfigured(
                f"tree_parent_field should be defined in {self.__class__}. Attribute '{self.TREE_PARENT_FIELD}'' not found"
            )

    @_parent.setter
    def _parent(self, value):
        """
        Allows to set _parent property

        Args:
            value (None): Relevant value from what TREE_PARENT_FIELD is defined

        Returns:
            None

        Raises:
            ImproperlyConfigured: When TREE_PARENT_FIELD if not relevant faced to the real class
        """
        field = hasattr(self, self.TREE_PARENT_FIELD)
        if field:
            setattr(self, self.TREE_PARENT_FIELD, value)
            return
        else:
            raise ImproperlyConfigured(
                f"tree_parent_field should be defined in {self.__class__}. Attribute '{self.TREE_PARENT_FIELD}'' not found"
            )

    def ensure_slug_unicity(self):
        """
        Ensure instance's slug is unique accross
        each model based on InternationalSlugMixin

        Raises:
            ValidationError: Used to raised the error in forms and serializer
        """
        for lang, code in self.languages:
            # We must test each langugages one by one to get detailed message
            ref_full_path_field_name, ref_full_path = self.get_international_field(
                "ref_full_path", lang
            )
            slug_field_name, slug = self.get_international_field("slug", lang)
            subclasses = InternationalSlugMixin.__subclasses__()
            site_filter = (
                {"sites__in": self.sites.all()}
                if self.pk is not None and hasattr(self, "sites")
                else {}
            )
            for cls in subclasses:
                qs = cls.objects.filter(
                    **site_filter, **{ref_full_path_field_name: ref_full_path}
                ).exclude(pk=self.pk)
                if qs.exists():
                    raise ValidationError(
                        _(
                            f"{slug} is invalid as a {cls.__name__} with full path {ref_full_path} already exists ({lang})"
                        )
                    )

    def slugify(self, created=False):
        """
        Slugify when required (auto_slug instance value)


        Args:
            created (bool, optional): When created is True, slug update will be enforced as long as auto_slug is defined for the language

        Raises:
            ImproperlyConfigured: Will be raised when SLUGIFY_FROM is not found on the model
        """
        if self.SLUGIFY_FROM is None or not hasattr(self, self.SLUGIFY_FROM):
            raise ImproperlyConfigured(
                f"slugify_from should be defined in {self.__class__}. Attribute '{self.SLUGIFY_FROM}' not found"
            )

        for lang, name in self.languages:
            # Define variables to increase code readibility
            slug_field_name, _slug = self.get_international_field("slug", lang)
            field_name, value = self.get_international_field(self.SLUGIFY_FROM, lang)
            auto_slug_field_name, _auto_slug = self.get_international_field(
                "auto_slug", lang
            )

            if (self.tracker.has_changed(field_name) or created) and _auto_slug:
                self.set_international_field("slug", lang, slugify(value))

    def denormalize_full_path(self, created=True, save=True, propagate=True):
        """
        Compute the instance's full path, and will propagate the modification accross the tree

        Args:
            created (bool, optional, default True): If True will enforce propagation, and forbid redirection creation
            save (bool, optional): Will call parent class save
            propagate (bool, optional): Will propagate modification accross tree
        """
        touched = False
        touched_full_path = []
        for lang, name in self.languages:
            ref_full_path_field_name, old_full_path = self.get_international_field(
                "ref_full_path", lang
            )
            new_full_path = self.full_path(lang)
            self.set_international_field("ref_full_path", lang, new_full_path)
            if self.tracker.has_changed(ref_full_path_field_name) or created:
                touched = True
                touched_full_path.append((old_full_path, new_full_path))

        if created:
            return Redirect.objects.filter(
                old_path__in=[new for old, new in touched_full_path],
                site_id=settings.SITE_ID,
            ).delete()
        if touched and (not created) and self.HANDLE_REDIRECTION_BOOL:
            handle_redirection(touched_full_path)

        if save and touched:
            super(InternationalSlugMixin, self).save()
        if propagate and touched and hasattr(self, "get_children") and save:
            for child in self.get_children():
                # We did not save modification yet, this allow to get the relevant full path
                child._parent = self
                child.denormalize_full_path(save=True, propagate=True)

    def full_path(self, lang):
        """
        Get full path in a specifi language as a function

        Args:
             lang (str): Language code - as defined in :django:topics:i18n.

        Returns:
            Returns the instance full path in the given language
            Exemple: /fr/omelette-et-du-fromage
        """
        slug_field_name, _slug = self.get_international_field("slug", lang)
        if self._parent is None:
            if _slug:
                return f"/{lang}/{_slug}/" if lang else f"/{_slug}/"
            else:
                return f"/{lang}/"
        else:
            parent_ref_full_path_field_name, parent_ref_full_path = self._parent.get_international_field(
                "ref_full_path", lang
            )
            return f"{parent_ref_full_path}{_slug}/"
