from django.test import TestCase
from stack_it.models import Page, PageTemplateContent


class PageTemplateContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello")
        PageTemplateContent.objects.create(path="path", key="key", value=page)
        self.assertEqual(PageTemplateContent.objects.count(), 1)
