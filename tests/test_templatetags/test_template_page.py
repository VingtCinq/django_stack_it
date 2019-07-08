from django.test import TestCase, RequestFactory
from django.template import Template, Context
from django.template.loader import get_template
from tests_utils.templates import compile_template
from stack_it.models import Page
from django.contrib.auth.models import AnonymousUser, User
from stack_it.models import Template as TemplateModel

from faker import Faker
from ddt import ddt, data


@ddt
class TemplatePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fake = Faker()
        cls.lambda_user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=fake.name()
        )

        cls.staff_user = User.objects.create_user(
            username=fake.name(),
            email=fake.email(),
            password=fake.name(),
            is_staff=True,
        )

    @classmethod
    def setUp(cls):
        cls.request_factory = RequestFactory()
        cls.connected_request = cls.request_factory.get(path="/")
        cls.connected_request.user = cls.lambda_user
        cls.staff_request = cls.request_factory.get(path="/")
        cls.staff_request.user = cls.staff_user
        cls.anonymous_request = cls.request_factory.get(path="/")
        cls.anonymous_request.user = AnonymousUser()

    @property
    def value_template(self):
        return Template(
            "{% load content_tags %}{% templatelink 'test' 'value' 'key' 'Hello World!' %}"
        )

    @property
    def meta_template(self):
        return Template(
            "{% load content_tags %}{% templatelink 'test' 'meta' 'key' 'Hello World!' %}"
        )

    @data(
        ("connected_request", compile_template("HelloWorld")),
        ("staff_request", get_template("stack_it/editable.html")),
        ("anonymous_request", compile_template("HelloWorld")),
    )
    def test_basic_value_creation(self, data):
        request_string, output = data
        rendered = self.value_template.render(
            Context({"request": getattr(self, request_string)})
        )
        template=TemplateModel.objects.get(path="test")
        self.assertEqual(template.contents.count(), 1)
        self.assertIn("key", template.values.keys(), template.values)
        # TODO Check content

    @data(
        ('connected_request', compile_template('HelloWorld')),
        ('staff_request', get_template('stack_it/editable.html')),
        ('anonymous_request', compile_template('HelloWorld')),
    )
    def test_basic_content_type_update(self, data):
        request_string, output = data
        self.meta_template.render(Context({
            'request': RequestFactory()
        }))
        rendered = self.value_template.render(Context({
            'request': getattr(self, request_string)
        }))
        template=TemplateModel.objects.get(path="test")

        self.assertEqual(template.contents.count(), 1)
        self.assertIn('key', template.values.keys(), template.metas)
        #TODO Check content

    # @data(
    #     ('connected_request', compile_template('OKAY')),
    #     ('staff_request', get_template('stack_it/editable.html')),
    #     ('anonymous_request', compile_template('OKAY')),
    # )
    # def test_content_modification(self, data):
    #     request_string, output = data
    #     page = Page.objects.create(title="My Title")
    #     self.meta_template.render(Context({
    #         'request': self.anonymous_request
    #     }))
    #     self.value_template.render(Context({
    #         'request': getattr(self, request_string)
    #     }))
    #     page.values.get('key').value = "OKAY"
    #     page.values.get('key').save()
    #     rendered = self.value_template.render(Context({
    #         'request': getattr(self, request_string)
    #     }))
    #     #TODO Check content
