from django.test import TestCase
from stack_it.models import Page, ModelPageContent


class ModelPageContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello")
        content = ModelPageContent.objects.create(key='key', page=page, instance_id=page.pk,
                                                  model_name='stack_it.Page')
        self.assertEqual(ModelPageContent.objects.count(), 1)
        self.assertEqual(set(ModelPageContent.objects.filter(pk__in=[content.pk])),
                         set(Page.objects.first().content_values))
