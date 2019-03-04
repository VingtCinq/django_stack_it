from django.db import connection
from modeltranslation.translator import translator, TranslationOptions
from django.test import TransactionTestCase


class AbstractModelTestMixin(TransactionTestCase):

    """
    A test mixin allowing you to test abstract models

    Attributes:
        extra_field (dict): Extra fields you want to add to your "real" model.
            example: {'title':models.CharField("Title", max_length=50)}
        mixin (Abstract Model): The Abstract model you want to test
        translation_fields (tuple): Fields you want to be translated with django-model-translations
    """

    mixin = None
    translation_fields = None
    extra_field = {}

    @classmethod
    def setUpClass(cls):
        super(AbstractModelTestMixin, cls).setUpClass()
        model_name = f'{cls.mixin.__name__}{cls.__name__}'
        attributes = {
            '__module__': 'stack_it',
        }
        attributes.update(cls.extra_field)
        cls.model = type(model_name,
                         (cls.mixin,),
                         attributes
                         )
        if cls.translation_fields:
            translator.register(cls.model, cls.translation_options())
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls.model)

    @classmethod
    def translation_options(self):
        attributes = {
            'fields': self.translation_fields
        }
        return type(f'{self.mixin.__name__}TranslationOptions', (TranslationOptions,), attributes)

