from django.db import models, transaction
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import Permission


class PermissionMixin(models.Model):
    """
    Simple mixin to handle permissions for objects
    """

    allowed_groups = models.ManyToManyField(
        "auth.Group",
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
        return self.allowed_groups.exists() == 0
