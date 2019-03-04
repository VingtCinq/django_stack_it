from django.test import SimpleTestCase
from stack_it.utils.templates import TemplateHelper
from django.conf import settings
import os


class TemplateHelloTest(SimpleTestCase):
    def test_template_list(self):
        FOLDERS = ['template_directory_for_test', 'template_sub_directory_for_test']
        helper = TemplateHelper(FOLDERS)
        self.assertEqual(set(helper.templates), set([
            os.path.join(settings.BASE_DIR, 'templates', *FOLDERS, 'test.html'),
            os.path.join(settings.BASE_DIR, 'templates', *FOLDERS, 'another_subdirectory', 'test.html'),
        ]))
