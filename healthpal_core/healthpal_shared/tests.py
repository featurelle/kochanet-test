from rest_framework.exceptions import ValidationError
from django.test import TestCase

class BaseSerializerTestCase(TestCase):
    """
    Base class for serializer tests that share common validation logic.\n
    Define both serializer_class and self.valid_data parameters in your subclass\n
    """

    serializer_class = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.serializer_class:
            raise ValueError(f"{cls.__name__} must define 'serializer_class'.")

    def _test_valid_data(self):
        """You should define self.valid_data in order to use this"""
        serializer = self.serializer_class(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def _test_invalid_data_part(self, invalid_data_part: dict):
        """You should define self.valid_data in order to use this"""
        invalid_data = self.valid_data.copy() | invalid_data_part
        serializer = self.serializer_class(data=invalid_data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

