from django.db import models
from django.utils.translation import ugettext_lazy as _
from stack_it.contents.abstracts import (
    BaseContentMixin,
    TextBaseContentMixin,
    ImageBaseContentMixin,
    PageBaseContentMixin,
    ModelBaseContentMixin,
)


class TemplateContent(BaseContentMixin):

    """
    Model for template related content
    BaseContentMixin is Polymorphic, allowing you to get all contents within few SQL queries (one per child models)

    Attributes:
        name (CharField): If you need to name your template for UX sugar
        path (CharField): Your template path, as used in "render" or include/extend
    """

    template = models.ForeignKey("stack_it.Template",verbose_name=_("Template"),related_name="contents", on_delete=models.CASCADE)

    class Meta:

        verbose_name = _('Template')
        verbose_name_plural = _('Template')
        unique_together = (('template', 'key'),)

    def __str__(self):
        return self.key

class TextTemplateContent(TemplateContent, TextBaseContentMixin):

    """
    See stack_it.contents.abstracts.TextBaseContentMixin for further details.
    Tests:
        tests.test_contents.models.templates.test_text_template_content
    """

    class Meta:
        verbose_name = _('Text Template Content')
        verbose_name_plural = _('Text Template Contents')


class ImageTemplateContent(TemplateContent, ImageBaseContentMixin):

    """
    See stack_it.contents.abstracts.ImageBaseContentMixin for further details.
    Tests:
        tests.test_contents.models.templates.test_image_template_content
    """

    class Meta:
        verbose_name = _('Image Template Content')
        verbose_name_plural = _('Image Template Contents')


class PageTemplateContent(TemplateContent, PageBaseContentMixin):

    """
    See stack_it.contents.abstracts.PageBaseContentMixin for further details.
    Tests:
        tests.test_contents.models.templates.test_page_template_content
    """

    class Meta:
        verbose_name = _('Related Page Template Content')
        verbose_name_plural = _('Related Page Template Contents')


class ModelTemplateContent(TemplateContent, ModelBaseContentMixin):

    """
    See stack_it.contents.abstracts.ModelPageContent for further details.
    Tests:
        tests.test_contents.models.templates.test_model_template_content
    """

    class Meta:
        verbose_name = _('Related Model Template Content')
        verbose_name_plural = _('Related Model Template Contents')
