from django.test import TestCase
from stack_it.models import Page, ModelTemplateContent


class ModelTemplateContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello")
        ModelTemplateContent.objects.create(key='key',
                                            path="template_path",
                                            instance_id=page.pk,
                                            model_name='stack_it.Page')
        self.assertEqual(ModelTemplateContent.objects.count(), 1)
