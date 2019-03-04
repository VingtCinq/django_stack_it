from django.utils.translation import ugettext_lazy as _
from django.db import models


class ImageRelatedMixin(models.Model):
    """
    A mixin to allow to track down which models uses an fk to "stack_it.Image"

    Attributes:
        image (ForeignKey to Image): Reference to the original image
        ref_alt (CharField): Denormalized image's alternative text
        ref_image (ImageField): Denormalized image's image file
    """

    image = models.ForeignKey("stack_it.Image", verbose_name=_("Image instance"), on_delete=models.CASCADE)
    ref_image = models.ImageField(_("Image"))
    ref_alt = models.CharField(_("Alternative text"), max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

    @classmethod
    def update_all(cls, image):
        """
        Method updating all real classes inherited from ImageRelatedMixin
        Used when an image is updated: each instance should be updated as ref_image and ref_alt are denormalized from image

        Args:
            image (stack_it.Image instance): All related "ImageRelatedMixin" related to this instance will be updated
        """
        subclasses = cls.__subclasses__()
        for cl in subclasses:
            if cl._meta.abstract:
                cl.update_all(image)
            else:
                cl.objects.filter(image=image).update(ref_image=image.image, ref_alt=image.alt)
