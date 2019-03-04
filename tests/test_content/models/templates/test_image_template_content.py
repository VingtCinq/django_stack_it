from django.test import TestCase
from stack_it.models import ImageTemplateContent
from stack_it.models import Image


class ImageTemplateContentModelTest(TestCase):
    def test_instance(self):
        img_name = 'test_image_is_denormalized_to_content_on_creation'
        image = Image.objects.create(image=Image.create_empty_image_file(name=img_name), alt="Hello")
        content = ImageTemplateContent.objects.create(path='template_name', key='key', image=image)
        self.assertEqual(ImageTemplateContent.objects.count(), 1)
