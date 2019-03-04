from stack_it.contents.abstracts import TextBaseContentMixin
from tests_utils.abstract_model_test_mixin import AbstractModelTestMixin


class TextBaseContentMixinUnitTest(AbstractModelTestMixin):
    """
    Testing TextBaseContentMixin
    Model is created by AbstractModelTestMixin.
    See tests_utils.abstract_model_test_mixin

    Attributes:
        mixin (AbstractModel): See tests_utils.abstract_model_test_mixin
    """
    mixin = TextBaseContentMixin

    def test_instance(self):
        self.model.objects.create(value='hello')
        self.assertEqual(self.model.objects.count(), 1)
