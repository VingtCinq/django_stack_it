from django.db import models, transaction
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import Permission


class PermissionMixin(models.Model):
    """
    Simple mixin to handle permissions for objects
    """

    PERMISSION_ADMIN_FIELDSET = (
        _("Permissions"),
        {
            "fields": ("login_required","allowed_groups",),
            "classes": ("collapse", "wide"),
            "description": _("Handle page's permissions"),
        },
    )
    login_required = models.BooleanField(_("Login required"), default=False)
    allowed_groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        verbose_name=_("Groups"),
        help_text=_(
            "Which groups are allowed to see the object, page is public if left empty"
        ),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(PermissionMixin, self).save(*args, **kwargs)

    def is_allowed(self, user):
        if self.is_public:
            return True
        elif user.is_authenticated:
            return (
                self.allowed_groups.filter(
                    pk__in=user.groups.all().values("pk")
                ).exists()
                or user.is_superuser
            )
        else:
            return False

    @property
    def is_public(self):
        if self.login_required:
            return False
        else:
            return self.allowed_groups.exists() == 0
