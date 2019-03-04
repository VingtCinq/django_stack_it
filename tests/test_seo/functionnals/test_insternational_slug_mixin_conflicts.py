import itertools
from ddt import ddt, data
from tests_utils.international_slug_mixin import InternationaSluglMixinTestMixin
from django.core.exceptions import ValidationError
# from django.db.utils import IntegrityError


@ddt
class InternationaSluglMixinFunctionnalConflictsTest(InternationaSluglMixinTestMixin):
    """
    Test Case handle all slug conflict cases.
    """

    @data(
        *itertools.product(
            ['slug_unicity_and_redirections', 'slug_unicity_no_redirections'],
            ['slug_unicity_and_redirections', 'slug_unicity_no_redirections'],

        )
    )
    def test_slug_unicity_raises_an_error(self, data):
        model_1, model_2 = [self.models.get(model_name) for model_name in data]
        model_1.objects.create(field_fr='Field FR 1', field_en_us='Field EN-US')
        with self.assertRaises(ValidationError):
            instance = model_2(field_fr='Field FR 1', field_en_us='Field EN-US 2')
            instance.clean()

        with self.assertRaises(ValidationError):
            instance = model_2(field_fr='Field FR', field_en_us='Field EN-US')
            instance.clean()
