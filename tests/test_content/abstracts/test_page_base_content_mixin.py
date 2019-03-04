from stack_it.contents.abstracts import PageBaseContentMixin
from tests_utils.abstract_model_test_mixin import AbstractModelTestMixin
from stack_it.models import Page


class PageBaseContentMixinUnitTest(AbstractModelTestMixin):

    """
    Testing PageBaseContentMixin
    Model is created by AbstractModelTestMixin.
    See tests_utils.abstract_model_test_mixin

    Attributes:
        mixin (AbstractModel): See tests_utils.abstract_model_test_mixin
    """

    
    mixin = PageBaseContentMixin

    def test_instance(self):
        """Summary
        """
        self.model.objects.create(value=Page.objects.create(title='hello'))
        self.assertEqual(self.model.objects.count(), 1)
