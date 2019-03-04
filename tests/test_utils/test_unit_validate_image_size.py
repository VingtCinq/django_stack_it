from unittest import TestCase
from ddt import ddt, data
from django.core.exceptions import ValidationError
from stack_it.utils.validators import (
    validate_image_size
)


@ddt
class ValidateImageSizeTest(TestCase):
    @data(
        '100X100',
        '100X100',
        '100 X 100',
        '100 X100',
        '100X 100',
        '100x100',
        '100x100',
        '100 x 100',
        '100 x100',
        '100x 100',

    )
    def test_sucesses(self, value):
        self.assertEqual(validate_image_size(value), '100x100')

    @data(
        'A100X100',
        '100XA100',
        '100A X 100',
        '100 X 100A',
        '100A X 100A',
        '100A X 100A',
        '1A00 X 100',
        '100 X 1A00',
        'A100x100',
        '100xA100',
        '100A x 100',
        '100 x 100A',
        '100A x 100A',
        '100A x 100A',
        '1A00 x 100',
        '100 x 1A00',
        'AxA',
        'AXA'
        'A x A',
        'A X A'
        'Ax A',
        'AX A'
        'A xA',
        'A XA'

    )
    def test_failues(self, value):
        with self.assertRaises(ValidationError):
            validate_image_size(value)
