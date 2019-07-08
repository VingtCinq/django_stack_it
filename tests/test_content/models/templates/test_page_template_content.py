from django.test import TestCase
from stack_it.models import Page, PageTemplateContent, Template


class PageTemplateContentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super(PageTemplateContentModelTest, cls).setUpTestData()
        cls.template = Template.objects.create(path="path")

    def test_instance(self):
        page = Page.objects.create(title="Hello")
        PageTemplateContent.objects.create(template=self.template, key="key", value=page)
        self.assertEqual(PageTemplateContent.objects.count(), 1)
