from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()


class AdminGenericFunctionalTestSet(TestCase):
    app_label = ''
    model_lower = ''

    def _get_url(self, slug, *args):
        return reverse(f"admin:{self.app_label}_{self.model_lower}_{slug}", args=(*args,))

    def _reverse(self, slug, *args):
        return reverse(f"admin:{slug}", args=(*args,))

    @classmethod
    def setUpTestData(cls):
        super(AdminGenericFunctionalTestSet, cls).setUpTestData()
        cls.username = "user"
        cls.admin_email = "myemail@superuser.com"
        cls.admin_password = "test_password_123"
        cls.admin_user = User.objects.create_superuser(
            username=cls.username, email=cls.admin_email, password=cls.admin_password)

    def setUp(self):
        self.client.login(username=self.username, email=self.admin_email, password=self.admin_password)

    def assertResultCount(self, response, n):
        self.assertIn('cl', response.context, 'No results found in context')
        self.assertEqual(
            response.context['cl'].result_count,
            n,
            response.context.get('cl')
        )


class AdminChangelistMixin(object):

    def test_can_access_changelist(self):
        url = self._get_url('changelist')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.request.get('PATH_INFO'), url)
        self.assertResultCount(response, 1)


class AdminAddMixin(object):

    def test_can_access_add(self):
        url = self._get_url('add')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.request.get('PATH_INFO'), url)

    def test_can_add_object(self):
        url = self._get_url('add')
        response = self.client.post(url,
                                    # content_type="application/x-www-form-urlencoded",
                                    follow=True,
                                    **self.add_request_args(),
                                    )
        self.assertEqual(response.status_code, 200, response.content)
        self.assertNotIn('adminform', response.context_data, "Admin form should not be found")
        self.assertEqual(response.request.get('PATH_INFO'), self._get_url('changelist'))
        self.assertEqual(self.model.objects.count(), 2)

    def add_request_args(self):
        form=self.admin.form(instance=self.obj).fields
        self.assertTrue(form.is_valid(), form.errors.as_json())
        return {'data': form.cleaned_data()}


class AdminHistoryMixin(object):

    def test_can_access_history(self):
        url = self._get_url('history', self.obj.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.request.get('PATH_INFO'), url)


class AdminDeleteMixin(object):

    def test_can_access_delete(self):
        url = self._get_url('delete', self.obj.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.request.get('PATH_INFO'), url)


class AdminChangeMixin(object):

    def test_can_access_change(self):
        url = self._get_url('change', self.obj.pk)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.request.get('PATH_INFO'), url)


class AdminFunctionalTestSet(AdminChangelistMixin,
                             AdminAddMixin,
                             AdminHistoryMixin,
                             AdminDeleteMixin,
                             AdminChangeMixin):
    pass
