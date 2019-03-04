from tests_utils.abstract_model_test_mixin import AbstractModelTestMixin
from stack_it.contents.abstracts import ModelBaseContentMixin
from stack_it.models import Page


class ModelBaseContentMixinUnitTest(AbstractModelTestMixin):

    """
    Testing ModelBaseContentMixin
    Model is created by AbstractModelTestMixin.
    See tests_utils.abstract_model_test_mixin

    Attributes:
        mixin (AbstractModel): See tests_utils.abstract_model_test_mixin
    """

    mixin = ModelBaseContentMixin

    def test_value_returns_relevant_instance(self):
        """
        Checking value returns the given instance
        """
        page = Page.objects.create(title="Title")
        instance = self.model.objects.create(
            instance_id=page.pk,
            model_name='stack_it.Page'
        )
        self.assertEqual(page, instance.value)

    def test_value_returns_none_when_instance_is_deleted(self):
        """
        Checking value returns None when instance is deleted
        and instance_id is set to None
        """
        page = Page.objects.create(title="Title")
        instance = self.model.objects.create(
            instance_id=page.pk,
            model_name='stack_it.Page'
        )
        page.delete()
        self.assertEqual(instance.value, None)
        self.assertEqual(instance.instance_id, None)

    def test_value_returns_none_when_model_does_not_exists(self):
        """
        Might appens during development cycle that a model is deleted.
        Makes sure you get "None"
        """
        page = Page.objects.create(title="Title")
        instance = self.model.objects.create(
            instance_id=page.pk,
            model_name='hello.World'
        )
        page.delete()
        self.assertEqual(instance.value, None)
