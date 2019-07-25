from django.contrib.redirects.models import Redirect
from ddt import ddt, data
from tests_utils.international_slug_mixin import InternationaSluglMixinTestMixin

@ddt
class InternationaSluglMixinFunctionnalRedirectionTest(InternationaSluglMixinTestMixin):
    """
    Test Case handle all Redirect cases.
    """

    @data(
        'slug_unicity_and_redirections',
        'slug_unicity_no_redirections',
        'no_slug_unicity_and_redirections',
        'no_slug_unicity_no_redirections'
    )
    def test_instance_creation_init_slug_with(self, model_name):
        instance = self.models.get(model_name).objects.create(field_fr='Field FR', field_en='Field en')
        self.assertEqual(instance.slug_fr, 'field-fr')
        self.assertEqual(instance.slug_en, 'field-en')

    @data(
        ('slug_unicity_and_redirections'),
        ('slug_unicity_no_redirections'),
        ('no_slug_unicity_and_redirections'),
        ('no_slug_unicity_no_redirections')
    )
    def test_instance_modification_updates_slug(self, model_name):
        instance = self.models.get(model_name).objects.create(
            field='Field', field_fr='Field FR', field_en='Field en')
        instance.field_fr = 'Slug FR'
        instance.save()
        self.assertEqual(instance.slug_fr, 'slug-fr')
        self.assertEqual(instance.slug_en, 'field-en')

    @data(
        'slug_unicity_no_redirections',
        'no_slug_unicity_no_redirections'
    )
    def test_instance_creation_do_not_create_redirection(self, model_name):
        self.models.get(model_name).objects.create(field='hello')
        self.assertEqual(Redirect.objects.count(), 0)

    @data(
        'slug_unicity_and_redirections',
        'no_slug_unicity_and_redirections'
    )
    def test_instance_modification_creates_redirection(self, model_name):
        instance = self.models.get(model_name).objects.create(field='hello')
        instance.field_fr = 'world fr'
        instance.save()
        self.assertEqual(Redirect.objects.filter(old_path='/fr/hello/').count(), 1)
        self.assertEqual(Redirect.objects.get(old_path='/fr/hello/').new_path, '/fr/world-fr/')
        instance.field_en = 'world en us'
        instance.save()
        self.assertEqual(Redirect.objects.count(), 2)

    @data(
        'slug_unicity_and_redirections',
        'no_slug_unicity_and_redirections'
    )
    def test_instance_multiple_modifications_create_multiple_redirections(self, model_name):
        instance = self.models.get(model_name).objects.create(field='hello')
        instance.field_fr = 'world_fr'
        instance.field_en = 'world_en'
        instance.save()
        self.assertEqual(Redirect.objects.count(), 2)

    @data(
        'slug_unicity_and_redirections',
        'no_slug_unicity_and_redirections'
    )
    def test_redirection_new_path_is_overriden(self, model_name):
        instance = self.models.get(model_name).objects.create(
            field_fr='Instance FR', field_en='Instance en')

        instance.field_fr = 'redirection-1-fr'
        instance.save()

        instance.field_fr = 'redirection-2-fr'
        instance.save()

        self.assertEqual(Redirect.objects.get(old_path='/fr/instance-fr/').new_path, '/fr/redirection-2-fr/')

    @data(
        'slug_unicity_and_redirections',
        'no_slug_unicity_and_redirections'
    )
    def test_redirection_new_path_is_overriden_on_update(self, model_name):
        instance = self.models.get(model_name).objects.create(
            field_fr='Instance FR', field_en='Instance en')

        instance.field_fr = 'redirection-1-fr'
        instance.save()

        instance.field_fr = 'redirection-2-fr'
        instance.save()

        self.assertEqual(Redirect.objects.get(old_path='/fr/instance-fr/').new_path, '/fr/redirection-2-fr/')

    @data(
        'slug_unicity_and_redirections',
        'no_slug_unicity_and_redirections'
    )
    def test_instance_with_colliding_redirection_deletes_redirection(self, model_name):
        instance = self.models.get(model_name).objects.create(
            field_fr='Instance FR', field_en='Instance en')
        fp = instance.full_path('fr')
        instance.field_fr = 'redirection-1-fr'
        instance.save()
        new_instance = self.models.get(model_name).objects.create(
            field_fr='Instance FR', field_en='Instance 2 en')

        self.assertEqual(new_instance.full_path('fr'), fp)
        self.assertEqual(Redirect.objects.count(), 0)
