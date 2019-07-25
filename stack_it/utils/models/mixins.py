"""Summary
"""
try:
    from modeltranslation.utils import build_localized_fieldname as original_build_localized_fieldname
except ImportError:
    def original_build_localized_fieldname(x): return x
from model_utils import FieldTracker
from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.conf import settings
from django.db import models


class AbstractFieldTracker(FieldTracker):
    def finalize_class(self, sender, name, **kwargs):
        self.name = name
        self.attname = '_%s' % name
        if not hasattr(sender, name):
            super(AbstractFieldTracker, self).finalize_class(sender, **kwargs)


class BaseModelMixin(TimeStampedModel):
    """
    Base model for django stackit

    Attributes:
        tracker: See django-models-utils docs for usage
    """
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """
        Work around to allow tracker field propagation
        through child classes

        see :
        - https://gist.github.com/sbnoemi/7618916
        - https://github.com/jazzband/django-model-utils/issues/155
        """
        tracker = AbstractFieldTracker()
        tracker.finalize_class(self.__class__, 'tracker')
        super(BaseModelMixin, self).__init__(*args, **kwargs)


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


def build_localized_fieldname(field_name, lang=None):
    if lang is not None:
        return original_build_localized_fieldname(field_name, lang)
    return field_name


class InternationalMixin(BaseModelMixin):
    """
    Mixins to get & set international fields easily.
    Used in vast majority in Django Rest Serializers & Forms, and Hanldy when testing translated models
    """
    class Meta:
        abstract = True

    @classproperty
    def languages(cls):
        if "modeltranslation" in settings.INSTALLED_APPS:
            languages = settings.LANGUAGES
        else:
            languages = [(None, None), ]
        return languages

    @classmethod
    def get_international_extra_kwargs(cls, fields):
        """
        Used for forms/drf serializers extra_kwargs
        Will result in a international dict giving everything you need to
        get consistent values for all translated widget fields

        Args:
            fields (list): List of tuples structured as ('field_name', kwargs)

        Returns:
            A dict you should drop the dict to extra_kwargs in forms/serializer metaclasses.
            Example: {
            'field_name_lang_code': {
                    'required' : True
                }
            }

        Tests
        -test_utils.test_unit_international_mixins.InternationalMixinsUnitTest.test_get_get_international_extra_kwargs

        """
        return dict(
            [
                (build_localized_fieldname(field, lang), kwargs)
                for lang, name in cls.languages for field, kwargs in fields
            ])

    @classmethod
    def get_international_field_names(cls, field_name):
        """
        Returns all translated field from a field name

        Args:
            field_name (str): The field name you'd like to get international fields name from

        Returns:
            A list of translated field_name
            Example:['field_name_fr', 'field_name_en']

        Tests
        -test_utils.test_unit_international_mixins.InternationalMixinsUnitTest.test_get_international_field_names
        """
        return [build_localized_fieldname(field_name, lang) for lang, name in cls.languages]

    @classmethod
    def get_international_field_name(cls, field_name, lang):
        """
        Return localized field name

        Args:
            field_name (str): Field name
            lang (str): Language code - as defined in :django:topics:i18n.

        Returns:
            A string, giving the name of the translated field
            Exemple: 'field_name_fr'

        """
        return build_localized_fieldname(field_name, lang)

    def get_international_field_value(self, field_name, lang):
        """
        Return localized field name

        Args:
            field_name (str): Field name
            lang (str): Language code - as defined in :django:topics:i18n.

        Returns:
            Current translated field value.
            Exemple: 'hello'

        """
        return getattr(self, self.get_international_field_name(field_name, lang))

    @classmethod
    def build_international_kwargs_from_value(cls, field_name, value):
        """Summary

        Args:
            field_name (str): Field name
            value (None): Any value corresponding to your field definition

        Returns:
            A dict you can pass to instanciate your model.
            Example: {
                    field_name_fr:"Bonjour",
                    field_name_en:"Bonjour"
                }
        """
        _dict = dict()
        for lang, name in cls.languages:
            intl_field_name = cls.get_international_field_name(field_name, lang)
            _dict.update({intl_field_name: value})
        return _dict

    def get_international_field(self, field_name, lang):
        """
        Returns translated field name

        Args:
            field_name (str): Field name
            lang (str): Language code - as defined in :django:topics:i18n.

        Returns:
            A tuple giving you the field name, and current field value.
            Example: ('field_name_fr', "Bonjour")
        """
        _field_name = build_localized_fieldname(field_name, lang)
        _field_value = getattr(self, _field_name)
        return _field_name, _field_value

    def set_international_field(self, field_name, lang, value):
        """
        Allows one to set a value in a given language

        Args:
            field_name (str): Field name
            lang (str): Language code - as defined in :django:topics:i18n.
            value (None): Any value corresponding to your field definition

        Returns:
            True
        """
        _field_name = build_localized_fieldname(field_name, lang)
        setattr(self, _field_name, value)
        return True

    def get_international_dict(self, field_name):
        """
        Gives you all field's available translation

        Args:
            field_name (str): Field name

        Returns:
            A dict giving you each translations's value.
            Example:
                {
                    'field_fr': "Bonjour",
                    'field_en': "World"
                }
        """
        return dict([self.get_international_field(field_name, lang) for lang, code in self.languages])
