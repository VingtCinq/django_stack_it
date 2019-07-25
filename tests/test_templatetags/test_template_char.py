from django.test import TestCase, RequestFactory
from django.template import Template, Context
from django.template.loader import get_template
from tests_utils.templates import compile_template
from django.contrib.auth.models import AnonymousUser, User
from faker import Faker
from ddt import ddt, data
from stack_it.models import Template as TemplateModel
from django.db import transaction


@ddt
class TemplageCharTest(TestCase):
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
            "{% load content_tags %}{% templatechar 'test' 'value' 'key' 'widget' 'HelloWorld' %}"
        )

    @property
    def meta_template(self):
        return Template(
            "{% load content_tags %}{% templatechar 'test' 'meta'  'key' 'widget' 'HelloWorld' %}"
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
        template = TemplateModel.objects.get(path="test")
        self.assertEqual(template.contents.count(), 1)
        self.assertIn("key", template.values.keys(), template.values)


    @data(
        ("connected_request", compile_template("HelloWorld")),
        ("staff_request", get_template("stack_it/editable.html")),
        ("anonymous_request", compile_template("HelloWorld")),
    )
    def test_basic_content_type_update(self, data):
        request_string, output = data
        self.meta_template.render(Context({"request": getattr(self, request_string)}))
        rendered = self.value_template.render(
            Context({"request": getattr(self, request_string)})
        )
        template = TemplateModel.objects.get(path="test")
        self.assertEqual(template.contents.count(), 1)
        self.assertIn("key", template.values.keys(), template.metas)


    @data(
        ("connected_request", compile_template("OKAY")),
        ("staff_request", get_template("stack_it/editable.html")),
        ("anonymous_request", compile_template("OKAY")),
    )
    def test_content_modification(self, data):
        request_string, output = data
        self.meta_template.render(Context({"request": getattr(self, request_string)}))
        self.value_template.render(Context({"request": getattr(self, request_string)}))
        template = TemplateModel.objects.get(path="test")
        template.values.get("key").value = "OKAY"
        template.values.get("key").save()
        del getattr(self, request_string).templates
        rendered = self.value_template.render(
            Context({"request": getattr(self, request_string)})
        )


