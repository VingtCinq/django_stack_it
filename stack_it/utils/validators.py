import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.apps import apps


def validate_image_size(value):
    pattern = re.compile("^\d+x\d+$")
    value = value.lower().replace(' ', '')
    if pattern.match(value.lower()):
        return value.lower()
    else:
        raise ValidationError(
            _('%(value)s do not match "size" format - witdhxheight (expressed in px)'),
            params={'value': value},
        )


def validate_model_name(value):
    app_label, model_name = value.split('.')
    models = [f'{model._meta.app_label}.{model.__name__}' for model in apps.get_models()]
    if value in models:
        return value
    else:
        raise ValidationError(
            _('%(value)s is not a valid model. Please choose within %(models)s'),
            params={'value': value, 'models': models},
        )
