from django.test import TestCase
from stack_it.models import Page, PageContent, TextPageContent
from django.db.utils import IntegrityError


class PageContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello")
        content = PageContent.objects.create(page=page)
        self.assertEqual(PageContent.objects.count(), 1)
        self.assertEqual(set(PageContent.objects.filter(pk__in=[content.pk])),
                         set(Page.objects.first().content_values))

    def test_conflict_over_multiple_models(self):
        page = Page.objects.create(title="Hello")
        PageContent.objects.create(page=page, key="key")
        with self.assertRaises(IntegrityError):
            content = TextPageContent.objects.create(page=page, key="key", value="value")
