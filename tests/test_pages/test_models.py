from django.test import TestCase
from stack_it.models import Page

class TextPageContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello", template_path="base.html",status=Page.PUBLISHED)
        page.sites.add(1)
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(str(page), "Hello")
        response = self.client.get(page.ref_full_path)
        self.assertEqual(response.status_code, 200, {'response': response.content, 'url': page.ref_full_path})
