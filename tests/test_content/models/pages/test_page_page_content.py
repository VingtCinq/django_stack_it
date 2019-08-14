from django.test import TestCase
from stack_it.models import Page, PagePageContent


class PagePageContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello")
        content = PagePageContent.objects.create(page=page, key="key", value=page)
        self.assertEqual(PagePageContent.objects.count(), 1)
        self.assertEqual(set(PagePageContent.objects.filter(pk__in=[content.pk])),
                         set(Page.objects.first().values))
