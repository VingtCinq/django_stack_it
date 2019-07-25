import logging
from django import template
from stack_it.models import (
    TextPageContent,
    ImagePageContent,
    PagePageContent,
    ModelPageContent,
    TextTemplateContent,
    ImageTemplateContent,
    PageTemplateContent,
    ModelTemplateContent,
    Template,
)
from stack_it.utils.templatetags.node_mixin import (
    ContentNodeMixin,
    TemplateContentNodeMixin,
    TextTagMixin,
    ImageTagMixin,
    PageTagMixin,
    get_template,
)

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()

# PAGE SECTION
class TextPageContentNode(ContentNodeMixin):
    CONTENT_MODEL = TextPageContent
    INSTANCE_PARAMETER_NAME = "page"


class CharPageContentNode(TextTagMixin):
    CONTENT_MODEL = TextPageContent
    INSTANCE_PARAMETER_NAME = "page"


class ImagePageContent(ImageTagMixin):
    CONTENT_MODEL = ImagePageContent
    INSTANCE_PARAMETER_NAME = "page"


class PagePageContent(PageTagMixin):
    CONTENT_MODEL = PagePageContent
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


@register.simple_tag(name="pagechar")
def pagechar(page, content_type, key, widget, content):
    text = CharPageContentNode(page, content_type, key, content)
    return text()


@register.simple_tag(name="pageimage")
def pageimage(page, content_type, key, size="800x600", color="0,0,0"):
    color = tuple([int(c) for c in color.split(",")])
    image = ImagePageContent(page, content_type, key, size, color)
    return image()


@register.simple_tag(name="pagelink")
def pagelink(page, content_type, key, title):
    page = PagePageContent(page, content_type, key, title)
    return page()


# PAGE SECTION
class TextTemplateContentNode(TemplateContentNodeMixin):
    CONTENT_MODEL = TextTemplateContent
    INSTANCE_PARAMETER_NAME = "template"


class CharTemplateContentNode(TextTagMixin):
    CONTENT_MODEL = TextTemplateContent
    INSTANCE_PARAMETER_NAME = "template"


class ImageTemplateContent(ImageTagMixin):
    CONTENT_MODEL = ImageTemplateContent
    INSTANCE_PARAMETER_NAME = "template"


class PageTemplateContent(PageTagMixin):
    CONTENT_MODEL = PageTemplateContent
    INSTANCE_PARAMETER_NAME = "template"


# TEMPLATE_SECTION


@register.tag(name="templatetext")
def templatetext(parser, token):
    nodelist = parser.parse(("endtemplatetext",))
    parser.delete_first_token()
    try:
        tag_name, templatename, content_type, key, widget = token.split_contents()
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

    if not (templatename[0] == templatename[-1] and templatename[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            f"templatename tag's argument should be in quotes: {templatename}"
        )
    else:
        templatename = templatename.strip('"').strip("'")

    return TextTemplateContentNode(templatename, content_type, key, widget, nodelist)


@register.simple_tag(name="templatechar", takes_context=True)
def templatechar(context, templatename, content_type, key, widget, content):
    request = context["request"]
    template = get_template(request, templatename)
    text = CharTemplateContentNode(template, content_type, key, content)
    return text()


@register.simple_tag(name="templateimage", takes_context=True)
def templateimage(
    context, templatename, content_type, key, size="800x600", color="0,0,0"
):
    request = context["request"]
    _template = get_template(request, templatename)
    color = tuple([int(c) for c in color.split(",")])
    image = ImageTemplateContent(_template, content_type, key, size, color)
    return image()


@register.simple_tag(name="templatelink", takes_context=True)
def templatelink(context, templatename, content_type, key, title):
    request = context["request"]
    _template = get_template(request, templatename)
    page = PageTemplateContent(_template, content_type, key, title)
    return page()
