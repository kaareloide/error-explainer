import unittest
from ..test_utils import run_test_scenario
from messages import get_formatted_message


class DefTest(unittest.TestCase):

    def test_assign_to_def(self):
        path = "tests/def_tests/samples/assign_to_def_error.py"
        expected_message = get_formatted_message("invalid_function_name.assign_to_def", line=3)
        run_test_scenario(self, path, 1, expected_message)

    def test_no_name_or_args_def(self):
        path = "tests/def_tests/samples/no_name_or_args_def_error.py"
        expected_message = get_formatted_message("missing_function_parts", line=3, invalid_def="def :")
        run_test_scenario(self, path, 1, expected_message)

    def test_no_name_or_args_def2(self):
        path = "tests/def_tests/samples/no_name_or_args_def_error2.py"
        expected_message = get_formatted_message("missing_function_parts", line=3, invalid_def="def name  :")
        run_test_scenario(self, path, 1, expected_message)

    def test_keyword_as_function_name(self):
        path = "tests/def_tests/samples/keyword_as_function_name_error.py"
        expected_message = get_formatted_message("invalid_function_name", line=3, invalid_name="pass")
        run_test_scenario(self, path, 1, expected_message)


if __name__ == '__main__':
    unittest.main()
