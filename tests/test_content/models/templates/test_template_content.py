from django.test import TestCase
from stack_it.models import Template, TemplateContent, TextTemplateContent
from django.db.utils import IntegrityError


class TemplateContentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateContentModelTest, cls).setUpTestData()
        cls.template = Template.objects.create(path="path")
        
    def test_instance(self):
        TemplateContent.objects.create(template=self.template)
        self.assertEqual(TemplateContent.objects.count(), 1)

    def test_conflict_over_multiple_models(self):
        TemplateContent.objects.create(template=self.template, key="key")
        with self.assertRaises(IntegrityError):
            TextTemplateContent.objects.create(
                template=self.template, key="key"
            )
