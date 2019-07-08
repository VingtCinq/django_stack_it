from polymorphic_tree.managers import PolymorphicMPTTModelManager
from django.db.models import Prefetch, Manager
from stack_it.utils.strings import pascalcase
from stack_it.contents.abstracts import BaseContentMixin
from stack_it.contents.models import PageContent, TemplateContent


class PageManager(PolymorphicMPTTModelManager):

    """
    Adding prefetchs for different content_types
    Tests:
        tests.test_pages.test_managers
    """

    def get_queryset(self):
        """
        Adding prefetchs for different each content_types
        Instances will come with relevant attrs, such as "content_values" and "content_metas"
        Returns:
            queryset: Whith relevent Prefetchs object added
        """
        return super(PageManager, self).get_queryset().prefetch_related(*self.prefetchs)

    @property
    def prefetchs(self):
        """
        Yields:
            Prefetch: A preftech object for each BaseContentMixin.CONTENT_TYPES
        """
        for content_type, txt in BaseContentMixin.CONTENT_TYPES:
            yield Prefetch(
                'contents',
                queryset=PageContent.objects.filter(content_type=content_type),
                to_attr=f'content_{content_type}s')

def status_manager_factory(status):
    """
    A Manager factory for status related manager.
    Usefull to easily create manager filtering on satus

    Args:
        status (str): Status value to filter on

    Returns:
        PageManager: adding a filter on status
    """

    def get_queryset(self):
        return super(PageManager, self).get_queryset().filter(status=status)
    return type(f'{pascalcase(status)}PageManager', (PageManager,), {'get_queryset': get_queryset})


class TemplateManager(Manager):

    """
    Adding prefetchs for different content_types
    Tests:
        tests.test_templates.test_managers
    """

    def get_queryset(self):
        """
        Adding prefetchs for different each content_types
        Instances will come with relevant attrs, such as "content_values" and "content_metas"
        Returns:
            queryset: Whith relevent Prefetchs object added
        """
        return super(TemplateManager, self).get_queryset().prefetch_related(*self.prefetchs)

    @property
    def prefetchs(self):
        """
        Yields:
            Prefetch: A preftech object for each BaseContentMixin.CONTENT_TYPES
        """
        for content_type, txt in BaseContentMixin.CONTENT_TYPES:
            yield Prefetch(
                'contents',
                queryset=TemplateContent.objects.filter(content_type=content_type),
                to_attr=f'content_{content_type}s')
