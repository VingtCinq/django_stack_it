from django.db import connection, models
from modeltranslation.translator import translator, TranslationOptions
from django.test import TransactionTestCase
from django.db.models.base import ModelBase
from stack_it.seo.mixins import InternationalSlugMixin
from django.apps import apps


class InternationalSlugMixinTranslation(TranslationOptions):
    fields = ('field', 'slug', 'auto_slug', 'ref_full_path')


class InternationaSluglMixinTestMixin(TransactionTestCase):
    mixin = InternationalSlugMixin

    @classmethod
    def build_model(cls,
                    ensure_slug_unicity_bool,
                    handle_redirection_bool):
        model_name = f'{cls.__name__}_{cls.mixin.__name__}_{ensure_slug_unicity_bool}_{handle_redirection_bool}'
        attributes = {
            '__module__': 'stack_it',
            'field': models.CharField("Test Field", max_length=50),
            'parent': models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True),
            'get_children': lambda x: x.children.all(),
            'SLUGIFY_FROM': 'field',
            'TREE_PARENT_FIELD': 'parent',
            'ENSURE_SLUG_UNICITY_BOOL': ensure_slug_unicity_bool,
            'HANDLE_REDIRECTION_BOOL': handle_redirection_bool
        }
        model = ModelBase(model_name,
                          (cls.mixin,),
                          attributes
                          )
        translator.register(model, InternationalSlugMixinTranslation)
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)
        return model

    @classmethod
    def setUpClass(cls):
        # Create a dummy model which extends the mixin
        super(InternationaSluglMixinTestMixin, cls).setUpClass()
        cls.models = {
            'slug_unicity_and_redirections': cls.build_model(True, True),
            'slug_unicity_no_redirections': cls.build_model(True, False),
            'no_slug_unicity_and_redirections': cls.build_model(False, True),
            'no_slug_unicity_no_redirections': cls.build_model(False, False),
        }

