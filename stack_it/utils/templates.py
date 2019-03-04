from django.conf import settings
from django.template.loaders.app_directories import get_app_template_dirs
import os


class TemplateHelper(object):

    def __init__(self, folder_conditions):
        super(TemplateHelper, self).__init__()
        self.folder_conditions = folder_conditions

    @property
    def base_template_dirs(self):
        for template_dir in get_app_template_dirs('templates'):
            yield template_dir
        for template_dir in settings.TEMPLATES[0]['DIRS']:
            yield template_dir

    @property
    def templates(self):
        return list(self.explore)

    @property
    def explore(self):
        for path in self.base_template_dirs:
            for root, dirs, files in os.walk(path):
                split_path = list(self.split(root))
                conditions = (path in split_path for path in self.folder_conditions)
                if all(path in list(split_path) for path in self.folder_conditions):
                    yield from [os.path.join(root, file) for file in files]

    def split(self, path):
        split_path = os.path.split(path)
        if split_path[0][-1] != os.sep:
            yield from self.split(split_path[0])
        yield split_path[1]
