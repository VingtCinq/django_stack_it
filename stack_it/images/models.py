"""Summary
"""
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.base import File
from django.utils.translation import ugettext_lazy as _
from stack_it.utils.models import BaseModelMixin
from django.db import models
from stack_it.images.mixins import ImageRelatedMixin


class Image(BaseModelMixin):

    """
    Model to handle all available images.
    No processors are to be stored here, as we want to keep orignal images.
    Processors should be handled in related instances. 
    See contents.abstracts.ImageBaseContent for an example

    Attributes:
        alt (CharField): Alternative text used for image description
        image (ImageField): Image source file
    """

    image = models.ImageField(_("Image"))
    alt = models.CharField(_("Alternative text"), max_length=50)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.alt

    def save(self, *args, **kwargs):
        """
        You want to update all instances related to current instance
        """
        super(Image, self).save(*args, **kwargs)
        if self.tracker.has_changed('image'):
            ImageRelatedMixin.update_all(self)

    @staticmethod
    def create_empty_image_file(name='test.jpeg', ext='jpeg', size=(1500, 1500), color=(256, 0, 0)):
        """Summary

        Args:
            name (str, optional): Description
            ext (str, optional): Description
            size (tuple, optional): Description
            color (tuple, optional): Description

        Returns:
            TYPE: Description
        """
        file_obj = BytesIO()
        image = PILImage.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)
