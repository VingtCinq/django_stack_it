from tests_utils.abstract_model_test_mixin import AbstractModelTestMixin
from stack_it.contents.abstracts import ImageBaseContentMixin
from stack_it.models import Image


class ImageBaseContentMixinUnitTest(AbstractModelTestMixin):
    """
    Testing ImageBaseContentMixin
    Model is created by AbstractModelTestMixin.
    See tests_utils.abstract_model_test_mixin
    
    Attributes:
        mixin (AbstractModel): See tests_utils.abstract_model_test_mixin
    """

    mixin = ImageBaseContentMixin

    def test_image_is_denormalized_to_content_on_creation(self):
        """
        Check image is imported from related image on creation
        """
        img_name = 'test_image_is_denormalized_to_content_on_creation'
        image = Image.objects.create(image=Image.create_empty_image_file(name=img_name), alt="Hello")
        image_content = self.model.objects.create(image=image)
        self.assertEqual(image_content.ref_image, image.image)
        self.assertEqual(image.alt, image_content.ref_alt)

    def test_image_is_denormalized_to_content_on_update(self):
        """
        Check image is imported from related image on update
        """
        img_name = 'test_image_is_denormalized_to_content_on_creation'
        image = Image.objects.create(image=Image.create_empty_image_file(name=img_name), alt="Hello")
        image_content = self.model.objects.create(image=image)
        image.image = Image.create_empty_image_file(name=f'{img_name}_2')
        image.alt = "World"
        image.save()
        image_content.refresh_from_db()
        self.assertEqual(image_content.ref_image, image.image)
        self.assertEqual(image.alt, image_content.ref_alt)

    def test_image_content_width(self):
        """
        Check width is computed correclty
        """
        img_name = 'test_image_content_creation_size'
        image = Image.objects.create(image=Image.create_empty_image_file(name=img_name), alt="Hello")
        image_content = self.model.objects.create(image=image, size="208x14")
        self.assertEqual(image_content.width, 208)

    def test_image_content_height(self):
        """
        Check height is computed correclty
        """
        img_name = 'test_image_content_creation_size'
        image = Image.objects.create(image=Image.create_empty_image_file(name=img_name), alt="Hello")
        image_content = self.model.objects.create(image=image, size="14x208")
        self.assertEqual(image_content.height, 208)

    def test_image_content_creation_size(self):
        """
        Check "value" returns an image according to model "size" parameters
        """
        img_name = 'test_image_content_creation_size'
        image = Image.objects.create(image=Image.create_empty_image_file(name=img_name), alt="Hello")
        image_content = self.model.objects.create(image=image, size="14x208")
        self.assertEqual(image_content.value.width, 14)
        self.assertEqual(image_content.value.height, 208)

