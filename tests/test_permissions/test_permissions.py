from stack_it.permissions.mixins import PermissionMixin
from tests_utils.abstract_model_test_mixin import AbstractModelTestMixin
from django.contrib.auth.models import AnonymousUser, User, Group
from django.contrib.auth.models import Permission


class PermissionMixinUnitTest(AbstractModelTestMixin):

    """
    Testing PermissionMixin
    Model is created by AbstractModelTestMixin.
    See tests_utils.abstract_model_test_mixin

    Attributes:
        mixin (AbstractModel): See tests_utils.abstract_model_test_mixin
    """

    mixin = PermissionMixin

    def test_is_public(self):
        obj = self.model.objects.create()
        self.assertTrue(obj.is_allowed(user=AnonymousUser()))

    def test_not_public_with_anonymous_user(self):
        obj = self.model.objects.create()
        self.assertFalse(obj.is_allowed(user=AnonymousUser()))

    def test_not_public_with_anonymous_user(self):
        group = Group.objects.create(name="Test")
        obj = self.model.objects.create()
        obj.allowed_groups.add(group)
        self.assertFalse(obj.is_allowed(user=AnonymousUser()))

    def test_not_public_with_not_allowed_user(self):
        user = User.objects.create()
        group = Group.objects.create(name="Test")

        obj = self.model.objects.create()
        obj.allowed_groups.add(group)

        self.assertFalse(obj.is_allowed(user=user))

    def test_not_public_with_allowed_user(self):
        user = User.objects.create()
        group = Group.objects.create(name="Test")
        user.groups.add(group)

        obj = self.model.objects.create()
        obj.allowed_groups.add(group)
        self.assertTrue(obj.is_allowed(user=user))
