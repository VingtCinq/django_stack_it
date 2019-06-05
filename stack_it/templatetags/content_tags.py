import logging
from django import template
from stack_it.models import (
    TextPageContent,
    ImagePageContent,
    PagePageContent,
    ModelPageContent,
)
from stack_it.utils.templatetags.node_mixin import ContentNodeMixin, ImageTagMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()


class TextPageContentNode(ContentNodeMixin):
    CONTENT_MODEL = TextPageContent
    INSTANCE_PARAMETER_NAME = "page"


class ImagePageContent(ImageTagMixin):
    CONTENT_MODEL = ImagePageContent
    INSTANCE_PARAMETER_NAME = "page"


@register.tag(name="pagetext")
def pagetext(parser, token):
    nodelist = parser.parse(("endpagetext",))
    parser.delete_first_token()
    try:
        tag_name, page, content_type, key, widget = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly 3 arguments" % token.contents.split()[0]
        )

    if not (content_type[0] == content_type[-1] and content_type[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            f"content_type tag's argument should be in quotes: {content_type}"
        )
    else:
        content_type = content_type.strip('"').strip("'")

    if not (key[0] == key[-1] and key[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            f"key tag's argument should be in quotes: {key}"
        )
    else:
        key = key.strip('"').strip("'")

    if not (widget[0] == widget[-1] and widget[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            f"widget tag's argument should be in quotes: {widget}"
        )
    else:
        widget = widget.strip('"').strip("'")

    return TextPageContentNode(page, content_type, key, widget, nodelist)


@register.simple_tag(name="pageimage")
def pageimage(page, content_type, key, size="800x600", color="0,0,0"):
    color = tuple([int(c) for c in color.split(",")])
    print(color)
    image = ImagePageContent(page, content_type, key, size, color)
    return image()
