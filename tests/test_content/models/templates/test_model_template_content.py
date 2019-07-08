from django.test import TestCase
from stack_it.models import Page, ModelTemplateContent, Template


class ModelTemplateContentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super(ModelTemplateContentModelTest, cls).setUpTestData()
        cls.template = Template.objects.create(path="path")

    def DONTtest_instance(self):
        page = Page.objects.create(title="Hello")
        ModelTemplateContent.objects.create(key='key',
                                            template=self.template,
                                            instance_id=page.pk,
                                            model_name='stack_it.Page')
        self.assertEqual(ModelTemplateContent.objects.count(), 1)
