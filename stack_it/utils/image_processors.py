from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill
from imagekit.utils import get_field_info


class ResizedImage(ImageSpec):
    format = 'JPEG'
    options = {'quality': 60}

    @property
    def processors(self):
        model, field_name = get_field_info(self.source)
        return [ResizeToFill(model.width, model.height)]


register.generator('utils:processors:resized_image', ResizedImage)
