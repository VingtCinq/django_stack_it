from django.test import TestCase
from stack_it.models import Image


class TextPageContentModelTest(TestCase):
    def test_instance(self):
        file = Image.create_empty_image_file(name='hello.jpg')
        image = Image.objects.create(image=file, alt="World")
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(str(image)[16:21], 'hello')
