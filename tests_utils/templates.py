from django.template.loader import _engine_list


def compile_template(template_string, using=None):
    """
    Load and return a template for the given string.
    """
    engines = _engine_list(using)
    for engine in engines:
        return engine.from_string(template_string)
