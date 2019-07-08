from django.test import TestCase
from stack_it.models import Page
from django.conf import settings

class TextPageContentModelTest(TestCase):
    def test_page_existence(self):
        page = Page.objects.create(title="Hello", template_path="base.html")
        response = self.client.get(page.ref_full_path)
        self.assertEqual(
            response.status_code,
            200,
            {"response": response.content, "url": page.ref_full_path},
        )

    def test_page_redirect(self):
        page = Page.objects.create(title="Hello", template_path="base.html")
        url = page.ref_full_path
        page.title = "New Title"
        page.save()
        response = self.client.get(url, follow=True)
        self.assertEqual(
            response.status_code,
            200,
            {"response": response.content, "url": page.ref_full_path},
        )
        self.assertIn(
            (page.ref_full_path, 301), response.redirect_chain, response.redirect_chain
        )

    def test_404(self):
        page = Page.objects.create(title="Hello", template_path="base.html")
        response = self.client.get("page.ref_full_path")
        self.assertEqual(response.status_code, 404)

