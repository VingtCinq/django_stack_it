from django.contrib.redirects.models import Redirect
from ddt import ddt, data
from tests_utils.international_slug_mixin import InternationaSluglMixinTestMixin


@ddt
class InternationaSluglMixinUnitTest(InternationaSluglMixinTestMixin):

    @data(
        'slug_unicity_and_redirections',
        'slug_unicity_no_redirections',
        'no_slug_unicity_and_redirections',
        'slug_unicity_no_redirections'
    )
    def test_slugify(self, model_name):
        instance = self.models.get(model_name).objects.create(
            field='Field', field_fr='Field FR', field_en_us='Field EN-US')
        self.assertEqual(instance.slug_fr, 'field-fr')
        self.assertEqual(instance.slug_en_us, 'field-en-us')

    @data(
        'slug_unicity_and_redirections',
        'slug_unicity_no_redirections',
        'no_slug_unicity_and_redirections',
        'slug_unicity_no_redirections'
    )
    def test_full_path_without_parent(self, model_name):
        instance = self.models.get(model_name).objects.create(
            field='Field', field_fr='Field FR', field_en_us='Field EN-US')
        self.assertEqual(instance.full_path('fr'), '/fr/field-fr/')
        self.assertEqual(instance.full_path('en-us'), '/en-us/field-en-us/')

    @data(
        'slug_unicity_and_redirections',
        'slug_unicity_no_redirections',
        'no_slug_unicity_and_redirections',
        'slug_unicity_no_redirections'
    )
    def test_full_path_with_parent_on_creation(self, model_name):
        model = self.models.get(model_name)
        parent = model.objects.create(field='parent', field_fr='parent FR', field_en_us='parent EN-US')
        instance = model.objects.create(parent=parent, field='instance',
                                        field_fr='instance FR', field_en_us='instance EN-US')
        self.assertEqual(instance.full_path('fr'), '/fr/parent-fr/instance-fr/')
        self.assertEqual(instance.full_path('en-us'), '/en-us/parent-en-us/instance-en-us/')

    @data(
        'slug_unicity_and_redirections',
        'slug_unicity_no_redirections',
        'no_slug_unicity_and_redirections',
        'slug_unicity_no_redirections'
    )
    def test_full_path_with_parent_on_update(self, model_name):
        model = self.models.get(model_name)
        parent = model.objects.create(field='parent', field_fr='parent FR', field_en_us='parent EN-US')
        instance = model.objects.create(parent=parent, field='instance',
                                        field_fr='instance FR', field_en_us='instance EN-US')
        parent.field_fr = 'new parent FR'
        parent.field_en_us = 'new parent EN-US'
        parent.save()
        instance.refresh_from_db()
        self.assertEqual(instance.full_path('fr'), '/fr/new-parent-fr/instance-fr/')
        self.assertEqual(instance.full_path('en-us'), '/en-us/new-parent-en-us/instance-en-us/')
