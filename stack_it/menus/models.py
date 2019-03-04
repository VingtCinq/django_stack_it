from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from stack_it.utils.models import BaseModelMixin


class Menu(BaseModelMixin, MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(_("Name"), max_length=150)

    page = models.ForeignKey(getattr(settings, 'PAGE_MODEL', 'stack_it.Page'),
                             verbose_name=_("Page"), related_name="menus",
                             blank=True, null=True,
                             on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

    def __str__(self):
        return self.name
