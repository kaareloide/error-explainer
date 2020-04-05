import unittest

from test.test_utils import run_test_scenario
from error_explainer.messages import get_formatted_message


class IndentationTest(unittest.TestCase):
    def test_no_new_indentation(self):
        path = "indentation_samples/no_new_indentation_error.py"
        expected_message = get_formatted_message(
            "invalid_indentation.4",
            line=3,
            error_line="pass",
            last_start_of_block="if True:",
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_higher_level_of_indent_with_no_start(self):
        path = "indentation_samples/higher_level_of_indent_with_no_start_error.py"
        expected_message = get_formatted_message(
            "invalid_indentation.1",
            line=4,
            error_line="      pass",
            last_start_of_block="if True:",
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_no_matching_indent_level(self):
        path = "indentation_samples/no_matching_indent_level_error.py"
        expected_message = get_formatted_message(
            "invalid_indentation.2", line=4, error_line="    pass"
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_non_indented_comment_after_statement(self):
        path = "indentation_samples/non_indented_comment_after_statement.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)

    def test_start_of_indentation_at_eof(self):
        path = "indentation_samples/start_of_indentation_at_eof_error.py"
        expected_message = get_formatted_message(
            "invalid_indentation.3", line=5, error_line="else:"
        )
        run_test_scenario(self, path, 1, expected_message)


if __name__ == "__main__":
    unittest.main()
