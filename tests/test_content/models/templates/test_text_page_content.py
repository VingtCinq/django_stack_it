from django.test import TestCase
from stack_it.models import Page, TextTemplateContent, Template


class TextTemplateContentModelTest(TestCase):
    def test_instance(self):
        content = TextTemplateContent.objects.create(template=Template.objects.create(path="path"), key="key", value="value")
        self.assertEqual(TextTemplateContent.objects.count(), 1)
