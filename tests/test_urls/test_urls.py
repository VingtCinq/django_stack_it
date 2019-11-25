from django.test import TestCase
from stack_it.models import Page
from django.conf import settings
from django.shortcuts import reverse
from django.utils.translation import activate


class UrlsTest(TestCase):
    def test_page_existence(self):
        page = Page.objects.create(
            title="Hello", template_path="base.html", status=Page.PUBLISHED
        )
        page.sites.add(1)
        response = self.client.get(page.ref_full_path)
        self.assertEqual(
            response.status_code,
            200,
            {"response": response.content, "url": page.ref_full_path},
        )

    def test_page_redirect(self):
        page = Page.objects.create(
            title="Hello", template_path="base.html", status=Page.PUBLISHED
        )
        page.sites.add(1)

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
        page = Page.objects.create(
            title="Hello", template_path="base.html", status=Page.PUBLISHED
        )
        page.sites.add(1)
        response = self.client.get("page.ref_full_path")
        self.assertEqual(response.status_code, 404)

    def test_key_url_reverse(self):
        page = Page.objects.create(
            title="Hello", template_path="base.html", status=Page.PUBLISHED
        )
        page.sites.add(1)
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(str(page), "Hello")
        response = self.client.get(page.ref_full_path)
        self.assertEqual(
            response.status_code,
            200,
            {"response": response.content, "url": page.ref_full_path},
        )
        self.assertEqual(reverse("stack_it:page", args=("hello",)), page.ref_full_path)

