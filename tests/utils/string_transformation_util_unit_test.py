from unittest import TestCase
from app.utils import pascal_to_snake_case

class TestStringTransformationUtil(TestCase):
    def test_pascal_to_snake_case(self) -> None:
        """
        All valid strings should be converted from pascal to snake case.
        :return:
        """
        self.assertEqual(pascal_to_snake_case('ThisIsATest'), 'this_is_a_test')
        self.assertEqual(pascal_to_snake_case('AnotherTest'), 'another_test')
        self.assertEqual(pascal_to_snake_case('TestModuleName'), 'test_module_name')