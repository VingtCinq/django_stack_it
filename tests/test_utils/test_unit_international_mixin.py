from tests_utils.abstract_model_test_mixin import AbstractModelTestMixin
from stack_it.utils.models.mixins import InternationalMixin
from django.db import models


class InternationalMixinUnitTest(AbstractModelTestMixin):
    mixin = InternationalMixin
    translation_fields = ('field',)
    extra_field = {'field': models.CharField("Test Field", max_length=50)}

    def test_get_international_extra_kwargs(self):
        rslt = {
            'field_fr': {'key': 'value'},
            'field_en_us': {'key': 'value'}
        }
        self.assertEqual(self.model.get_international_extra_kwargs([('field', {'key': 'value'}), ]), rslt)

    def test_get_international_field_names(self):
        rslt = set(['field_fr', 'field_en_us'])
        self.assertEqual(set(self.model.get_international_field_names('field')), rslt)

    def test_get_international_field(self):
        instance = self.model.objects.create(
            field_fr="Bonjour",
            field_en_us="World"
        )
        self.assertEqual(instance.get_international_field('field', 'fr'), ("field_fr", "Bonjour"))
        self.assertEqual(instance.get_international_field('field', 'en-us'), ("field_en_us", "World"))

    def test_set_international_field(self):
        instance = self.model.objects.create(
            field_fr="Bonjour",
            field_en_us="World"
        )
        instance.set_international_field(field_name='field', lang='fr', value="Omelette et du fromage")
        self.assertEqual(instance.field_fr, "Omelette et du fromage")

    def test_get_international_dict(self):
        instance = self.model.objects.create(
            field_fr="Bonjour",
            field_en_us="World"
        )
        rslt = {
            'field_fr': "Bonjour",
            'field_en_us': "World"
        }
        self.assertEqual(instance.get_international_dict('field'), rslt)

    def test_get_international_field_name(self):
        self.assertEqual(self.model.get_international_field_name('field', 'fr'), 'field_fr')
        self.assertEqual(self.model.get_international_field_name('field', 'en-us'), 'field_en_us')

    def test_build_international_kwargs_from_value(self):
        rslt = {
            'field_fr': "hello",
            'field_en_us': "hello"
        }
        self.assertEqual(self.model.build_international_kwargs_from_value('field', 'hello'), rslt)

    def test_get_international_field_value(self):
        instance = self.model.objects.create(
            field_fr="Bonjour",
            field_en_us="World"
        )
        self.assertEqual(instance.get_international_field_value('field', 'fr'), 'Bonjour')
        self.assertEqual(instance.get_international_field_value('field', 'en-us'), 'World')
