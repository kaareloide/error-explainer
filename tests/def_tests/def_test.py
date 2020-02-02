import unittest
from ..test_utils import run_test_scenario
from message_provider import MessageProvider


class DefTest(unittest.TestCase):

    def setUp(self):
        self.message_provider = MessageProvider()
        self.message_provider.parse_messages()

    def test_assign_to_def(self):
        missing_colon_after_if_path = "tests/def_tests/samples/assign_to_def_error.py"
        # todo wrong line location for some reason
        expected_message = self.message_provider.get_formatted_message("invalid_function_name.assign_to_def", line=2)
        run_test_scenario(self, missing_colon_after_if_path, 1, expected_message)

    def test_no_name_or_args_def(self):
        # todo
        missing_colon_after_if_path = "tests/def_tests/samples/no_name_or_args_def_error.py"
        expected_message = self.message_provider.get_formatted_message("missing_function_parts",
                                                                       line=2, invalid_def="def :")
        run_test_scenario(self, missing_colon_after_if_path, 1, expected_message)

    def test_no_name_or_args_def2(self):
        # todo
        missing_colon_after_if_path = "tests/def_tests/samples/no_name_or_args_def_error2.py"
        expected_message = self.message_provider.get_formatted_message("missing_function_parts",
                                                                       line=3, invalid_def="def name  :")
        run_test_scenario(self, missing_colon_after_if_path, 1, expected_message)

    def test_keyword_as_function_name(self):
        # todo
        missing_colon_after_if_path = "tests/def_tests/samples/keyword_as_function_name_error.py"
        expected_message = self.message_provider.get_formatted_message("invalid_function_name",
                                                                       line=2, invalid_name="pass")
        run_test_scenario(self, missing_colon_after_if_path, 1, expected_message)


if __name__ == '__main__':
    unittest.main()
