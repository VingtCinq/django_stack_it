from stack_it.contents.abstracts import BaseContentMixin
from tests_utils.abstract_model_test_mixin import AbstractModelTestMixin


class ModelBaseContentMixinUnitTest(AbstractModelTestMixin):

    """
    Testing BaseContentMixin
    Model is created by AbstractModelTestMixin.
    See tests_utils.abstract_model_test_mixin

    Attributes:
        mixin (AbstractModel): See tests_utils.abstract_model_test_mixin
    """

    mixin = BaseContentMixin

    def test_instance(self):
        self.model.objects.create(key='hello')
        self.assertEqual(self.model.objects.count(), 1)
