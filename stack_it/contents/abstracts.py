"""
Abstracts models used to create content related models easiliy

"""
from django.db import models
from stack_it.utils.models.mixins import BaseModelMixin
from stack_it.utils.validators import validate_image_size, validate_model_name
from polymorphic.models import PolymorphicModel
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
from imagekit.models import ImageSpecField
from stack_it.images.mixins import ImageRelatedMixin


class BaseContentMixin(BaseModelMixin, PolymorphicModel):

    """
    BaseContentMixin real model will be inherited themselves.
    That will allow much easier query behavior

    Attributes:
        content_type (CharField): Define if current content if used as regular content or "Meta"
            For a page, you might want to define some parameters, like, a number of post to display, called "nb_posts".
            This "nb_posts" shouldn't be available within the template directly. Specific UX should be designed to handle thos king of data
        key (CharField): Stack It Content management is based on key-value pairs. While we don't now what the value will be, we certainly know 
            which form the key should have.

        META (str): Value when content is Meta. See content_type definition for further explanation
        VALUE (str): Value when content is Content.See content_type definition for further explanation
        CONTENT_TYPES (tuple): Gather all available content types, to make them available within content_type choices

    Tests:
        test.test_content.abstract.test_base_content_mixin
    """

    META = "meta"
    VALUE = "value"

    CONTENT_TYPES = ((META, _("Meta content")), (VALUE, _("Standard content")))
    key = models.CharField(_("Key"), max_length=50, blank=False)
    content_type = models.CharField(
        _("Content Type"), max_length=50, choices=CONTENT_TYPES, default=VALUE
    )

    class Meta:
        abstract = True


class TextBaseContentMixin(models.Model):

    """
    TextBaseContentMixin will be injected into real models when content is text based

    Attributes:
        value (TextField): Will store textual values

    Tests:
        test.test_content.abstract.test_text_base_content_mixin

    """

    value = models.TextField(_("Value"))

    class Meta:
        abstract = True


class ImageBaseContentMixin(ImageRelatedMixin):

    """
    ImageBaseContentMixin will be injected into real models when content is an image

    Attributes:
        image (ForeignKey to Image): See stack_it.images.mixins.ImageRelatedMixin
        ref_alt (CharField): See stack_it.images.mixins.ImageRelatedMixin
        ref_image (ImageField): See stack_it.images.mixins.ImageRelatedMixin

        size (CharField): Gives wanted image size
        value (ImageSpecField): Store the resized image

    Tests:
        test.test_content.abstract.test_image_base_content_mixin

    """

    size = models.CharField(
        _("Size"), max_length=50, default="800x600", validators=[validate_image_size]
    )
    value = ImageSpecField(source="ref_image", id="utils:processors:resized_image")

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ImageBaseContentMixin, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Denormalize image information
        """
        self.ref_image = self.image.image
        self.ref_alt = self.image.alt
        super(ImageBaseContentMixin, self).save(*args, **kwargs)

    @property
    def parsed_size(self):
        """
        Parse model's size field

        Returns:
            tuple: (width,heigt)
        """
        return tuple((int(size) for size in self.size.split("x")))

    @property
    def width(self):
        return self.parsed_size[0]

    @property
    def height(self):
        return self.parsed_size[1]

    @property
    def url(self):
        return self.value.url

    @classmethod
    def init(cls, **kwargs):
        from stack_it.models import Image

        try:
            color = kwargs.pop("color")
        except KeyError:
            color = (0, 0, 0)
        content = cls(**kwargs)
        image = Image.init_image(
            name="init-{key}-{size}.jpg".format(**kwargs),
            size=content.parsed_size,
            color=color,
        )
        content.image = image
        content.save()
        return content


class PageBaseContentMixin(models.Model):

    """
    PageBaseContentMixin will be injected into real models when content is a Page
    Please keep in mind Page is polymorphic, and anything showing of on your webapp should inherit from Page

    Attributes:
        value (ForeignKey): Will stock related page's ID

    Tests:
        test.test_content.abstract.test_page_base_content_mixin

    """

    value = models.ForeignKey(
        "stack_it.Page",
        related_name="related_%(class)s",
        verbose_name=_("Page"),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class ModelBaseContentMixin(models.Model):

    """
    ModelBaseContentMixin will be injected into real models when content is a something else.
    Obviously you did'nt want to inherit from Page, so... we'll let you do whatever you want.
    Not tested, you might want to avoid that...

    Attributes:
        instance_id (IntegerField): Will stock related page's ID
        model_name (CharField): Gives the model_name where you want to get your instance from

    Tests:
        test.test_content.abstract.test_model_base_content_mixin

    """

    instance_id = models.IntegerField(_("Object id"), null=True)
    model_name = models.CharField(
        _("Model Name"), max_length=50, validators=[validate_model_name]
    )

    class Meta:
        abstract = True

    @property
    def model(self):
        app_name, model_name = self.model_name.split(".")
        try:
            return apps.get_model(app_label=app_name, model_name=model_name)
        except LookupError:
            return None

    @property
    def value(self):
        if self.model is not None:

            try:
                return self.model.objects.get(pk=self.instance_id)
            except self.model.DoesNotExist:
                if self.instance_id is not None:
                    self.instance_id = None
                    self.save()
                return None
        return None
