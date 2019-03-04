from django.test import TestCase
from stack_it.models import TemplateContent, TextTemplateContent
from django.db.utils import IntegrityError


class TemplateContentModelTest(TestCase):
  def test_instance(self):
    TemplateContent.objects.create(path="path")
    self.assertEqual(TemplateContent.objects.count(), 1)

  def test_conflict_over_multiple_models(self):
    TemplateContent.objects.create(path="path")
    with self.assertRaises(IntegrityError):
      TextTemplateContent.objects.create(
          path="path",
          key="key",
          value="value")
