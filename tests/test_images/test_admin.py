import copy
from django.contrib import admin
from stack_it.models import Image
from stack_it.admin import ImageAdmin
from stack_it.images.forms import ImageForm
from tests_utils.admin import AdminGenericFunctionalTestSet, AdminFunctionalTestSet
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.db.models import Max

class ImageAdminTest(AdminGenericFunctionalTestSet, AdminFunctionalTestSet):
    app_label = 'stack_it'
    model_lower = 'image'
    model = Image
    admin = ImageAdmin

    @classmethod
    def setUpTestData(cls):
        admin.register(Image, ImageAdmin)
        super(ImageAdminTest, cls).setUpTestData()
        cls.obj = Image.objects.create(image=Image.create_empty_image_file(name='hello.jpg'), alt="World")

    # @property
    # def add_request_args(self):
    #     raise NotImplementedError

    def test_autocomplete(self):
        url = f"{self._get_url('autocomplete')}"
        response = self.client.get(url + "?term=hello", follow=True)
        self.assertEqual(response.request.get('PATH_INFO'), url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1, response.content)


    def test_get_on_image_upload_returns_404(self):
        url = self._get_url('image_upload')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, response.content)

    def test_get_on_delete_upload_returns_404(self):
        url = self._get_url('image_delete', self.obj.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, response.content)


    def test_valid_post_on_image_upload_creates_instance(self):
        url = self._get_url('image_upload')
        response = self.client.post(url,
                                    # content_type="application/x-www-form-urlencoded",
                                    follow=True,
                                    **self.add_request_args(),
                                    )
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(self.model.objects.count(), 2)

    def test_invalid_post_on_image_upload_does_not_create_instance(self):
        url = self._get_url('image_upload')
        response = self.client.post(url,
                                    data={},
                                    follow=True,
                                    )
        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(self.model.objects.count(), 1)


    def test_valid_post_on_image_deletes_pk(self):
        to_delete=Image.objects.create(image=Image.create_empty_image_file(name='to_delete.jpg'), alt="To Delete")
        url = self._get_url('image_delete', to_delete.pk)
        self.assertEqual(self.model.objects.count(), 2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(self.model.objects.count(), 1)

    def test_inexisting_post_on_image_delete_returns_404(self):
        pk=Image.objects.all().aggregate(Max('id'))['id__max']+1
        url = self._get_url('image_delete', pk)
        response = self.client.post(url,)
        self.assertEqual(response.status_code, 404, response.content)
        self.assertEqual(self.model.objects.count(), 1)

    def add_request_args(self):
        form = ImageForm(
            data={'folder': settings.BASE_FOLDER, },
            files={'image': Image.create_empty_image_file(), })
        self.assertTrue(form.is_valid(), form.errors)
        return {'data': form.cleaned_data, 'format': 'multipart'}
