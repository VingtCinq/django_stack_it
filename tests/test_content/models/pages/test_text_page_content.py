from django.test import TestCase
from stack_it.models import Page, TextPageContent


class TextPageContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello")
        content = TextPageContent.objects.create(page=page, key="key", value="value")
        self.assertEqual(TextPageContent.objects.count(), 1)
        self.assertEqual(set(TextPageContent.objects.filter(pk__in=[content.pk])),
                         set(Page.objects.first().values.values()))
