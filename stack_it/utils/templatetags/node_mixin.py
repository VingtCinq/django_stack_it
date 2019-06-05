import logging
from django import template
from stack_it.contents.abstracts import BaseContentMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()


class ContentNodeMixin(template.Node):
    CONTENT_MODEL = None
    ADMIN_TEMPLATE = "stack_it/editable.html"
    INSTANCE_PARAMETER_NAME = None

    def __init__(self, instance, content_type, key, widget, nodelist):
        super(ContentNodeMixin, self).__init__()
        self.instance = template.Variable(instance)
        self.key = key
        self.widget = widget
        self.nodelist = nodelist
        self.messages = []
        self.content_type = content_type
        self.alternative_content_types = list(
            dict(BaseContentMixin.CONTENT_TYPES).keys()
        )
        self.alternative_content_types.remove(self.content_type)
        self.admin_template = template.loader.get_template(self.ADMIN_TEMPLATE)

    def create_content(self, instance, content_type, key, value):
        """
        Creates related content
        This is meant to be overriden

        Returns:
            CONTENT_MODEL instance: Returns the CONTENT_MODEL instance which's just been created
        """
        attrs = dict(
            [
                (self.INSTANCE_PARAMETER_NAME, instance),
                ("content_type", content_type),
                ("key", key),
                ("value", value),
            ]
        )
        content_instance = self.CONTENT_MODEL.objects.create(**attrs)
        getattr(instance, f"{self.content_type}s").update(
            dict(((self.key, content_instance),))
        )
        return content_instance

    def content(self, context):
        instance = self.instance.resolve(context)
        original_output = self.nodelist.render(context)

        if self.key in getattr(instance, f"{self.content_type}s").keys():
            return getattr(instance, f"{self.content_type}s").get(self.key)

        for content_type in self.alternative_content_types:
            # Checking the key cannot be found anywhere else®
            if self.key in getattr(instance, f"{content_type}s").keys():
                content_instance = getattr(instance, f"{content_type}s").get(self.key)
                content_instance.content_type = self.content_type
                content_instance.save()
                msg = (
                    "warning",
                    f"Automatically changed {self.key} for instance {content_instance}!",
                )
                self.messages.append(msg)
                getattr(instance, f"{content_type}s").pop(self.key)
                getattr(instance, f"{self.content_type}s").update(
                    {self.key: content_instance}
                )
                return content_instance

        return self.create_content(
            instance, self.content_type, self.key, original_output
        )

    def render(self, context):
        content = self.content(context)
        if context["request"].user.is_staff:
            return self.admin_template.render(
                {
                    "id": content.id,
                    "key": self.key,
                    "widget": self.widget,
                    "value": content.value,
                }
            )
        return content.value


class ImageTagMixin(object):
    CONTENT_MODEL = None
    ADMIN_TEMPLATE = "stack_it/editable.html"
    INSTANCE_PARAMETER_NAME = None

    def __init__(self, instance, content_type, key, size, color):
        super(ImageTagMixin, self).__init__()
        self.instance = instance
        self.key = key
        self.size = size
        self.color = color
        self.messages = []
        self.content_type = content_type
        self.alternative_content_types = list(
            dict(BaseContentMixin.CONTENT_TYPES).keys()
        )
        self.alternative_content_types.remove(self.content_type)
        self.admin_template = template.loader.get_template(self.ADMIN_TEMPLATE)

    def create_content(
        self, instance, content_type, key, size="800x600", color=(0, 0, 0)
    ):
        """
        Creates related content
        This is meant to be overriden

        Returns:
            CONTENT_MODEL instance: Returns the CONTENT_MODEL instance which's just been created
        """
        attrs = dict(
            [
                (self.INSTANCE_PARAMETER_NAME, instance),
                ("content_type", content_type),
                ("key", key),
                ("size", size),
                ("color", color),
            ]
        )
        content_instance = self.CONTENT_MODEL.init(**attrs)
        getattr(instance, f"{self.content_type}s").update(
            dict(((self.key, content_instance),))
        )
        return content_instance

    def __call__(self):
        instance = self.instance

        if self.key in getattr(instance, f"{self.content_type}s").keys():
            return getattr(instance, f"{self.content_type}s").get(self.key)

        for content_type in self.alternative_content_types:
            # Checking the key cannot be found anywhere else®
            if self.key in getattr(instance, f"{content_type}s").keys():
                content_instance = getattr(instance, f"{content_type}s").get(self.key)
                content_instance.content_type = self.content_type
                content_instance.save()
                msg = (
                    "warning",
                    f"Automatically changed {self.key} for instance {content_instance}!",
                )
                self.messages.append(msg)
                getattr(instance, f"{content_type}s").pop(self.key)
                getattr(instance, f"{self.content_type}s").update(
                    {self.key: content_instance}
                )
                return content_instance

        return self.create_content(
            instance, self.content_type, self.key, self.size, self.color
        )
