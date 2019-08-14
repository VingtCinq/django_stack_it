from django.test import TestCase
from stack_it.models import Page, ImagePageContent
from stack_it.models import Image


class ImagePageContentModelTest(TestCase):
    def test_instance(self):
        page = Page.objects.create(title="Hello")
        img_name = 'test_image_is_denormalized_to_content_on_creation'
        image = Image.objects.create(image=Image.create_empty_image_file(name=img_name), alt="Hello")
        content = ImagePageContent.objects.create(page=page, key='key', image=image)
        self.assertEqual(ImagePageContent.objects.count(), 1)
        self.assertEqual(set(ImagePageContent.objects.filter(pk__in=[content.pk])),
                         set(Page.objects.first().values.values()))
