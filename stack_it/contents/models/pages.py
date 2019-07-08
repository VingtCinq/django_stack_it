from django.db import models
from django.utils.translation import ugettext_lazy as _
from stack_it.contents.abstracts import (
    BaseContentMixin,
    TextBaseContentMixin,
    ImageBaseContentMixin,
    PageBaseContentMixin,
    ModelBaseContentMixin,
)


class PageContent(BaseContentMixin):

    """
    Model for page related content
    BaseContentMixin is Polymorphic, allowing you to get all contents within few SQL queries (one per child models)

    Attributes:
        page (ForeignKey): Page instance where content belongs
    """

    page = models.ForeignKey(
        "stack_it.Page",
        verbose_name=_("Page"),
        related_name="contents",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Page Content")
        verbose_name_plural = _("Page Contents")
        unique_together = (("page", "key"),)


class TextPageContent(PageContent, TextBaseContentMixin):

    """
    See stack_it.content.abstracts.TextBaseContentMixin for further details.
    Tests:
        tests.test_contents.models.pages.test_text_page_content
    """

    class Meta:
        verbose_name = _("Text Page Content")
        verbose_name_plural = _("Text Page Contents")


class ImagePageContent(PageContent, ImageBaseContentMixin):

    """
    See stack_it.content.abstracts.ImageBaseContentMixin for further details.
    Tests:
        tests.test_contents.models.pages.test_image_page_content
    """

    class Meta:
        verbose_name = _("Image Page Content")
        verbose_name_plural = _("Image Page Contents")


class PagePageContent(PageContent, PageBaseContentMixin):

    """
    See stack_it.content.abstracts.PageBaseContentMixin for further details.
    Tests:
        tests.test_contents.models.pages.test_page_page_content
    """

    class Meta:
        verbose_name = _("Related Page Page Content")
        verbose_name_plural = _("Related Page Page Contents")

    
class ModelPageContent(PageContent, ModelBaseContentMixin):

    """
    See stack_it.content.abstracts.ModelPageContent for further details.
    Tests:
        tests.test_contents.models.pages.test_model_page_content
    """

    class Meta:
        verbose_name = _("Related Model Page Content")
        verbose_name_plural = _("Related Model Page Contents")
