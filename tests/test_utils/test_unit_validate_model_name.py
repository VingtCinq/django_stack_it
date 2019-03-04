from unittest import TestCase
from django.apps import apps
from ddt import ddt, data
from django.core.exceptions import ValidationError
from stack_it.utils.validators import (
    validate_model_name
)


@ddt
class ValidateModelNameTest(TestCase):

    @data(*[f'{model._meta.app_label}.{model.__name__}' for model in apps.get_models()])
    def test_model_name_validation_passes(self, model_name):
        self.assertEqual(validate_model_name(model_name), model_name)

    def test_model_name_validation_raises_an_error(self):
        with self.assertRaises(ValidationError):
            validate_model_name('hello.World')

