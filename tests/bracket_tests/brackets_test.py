import unittest
from ..test_utils import run_test_scenario
from messages import get_formatted_message


class BracketsTest(unittest.TestCase):

    def test_missing_bracket_after(self):
        missing_bracket_after_path = "tests/bracket_tests/samples/missing_bracket_after_error.py"
        expected_message = get_formatted_message("missing_brackets.normal.closing", count=1, line=2)
        run_test_scenario(self, missing_bracket_after_path, 1, expected_message)

    def test_miss_matched_bracket_types(self):
        miss_matched_bracket_path = "tests/bracket_tests/samples/miss_matched_bracket_error.py"
        expected_message = get_formatted_message("miss_matched_brackets.square.normal", line=2)
        run_test_scenario(self, miss_matched_bracket_path, 1, expected_message)

    def test_miss_matched_bracket_types_multiline(self):
        miss_matched_bracket_path_multiline = "tests/bracket_tests/samples/miss_matched_bracket_multiline_error.py"
        expected_message = get_formatted_message("miss_matched_brackets.square.normal", line=2)
        run_test_scenario(self, miss_matched_bracket_path_multiline, 1, expected_message)

    def test_missing_brackets_print(self):
        missing_bracket_print_path = "tests/bracket_tests/samples/missing_brackets_print_error.py"
        expected_message = get_formatted_message("missing_brackets.print", line=2)
        run_test_scenario(self, missing_bracket_print_path, 1, expected_message)

    def test_missing_square_bracket_after(self):
        missing_square_bracket_after_path = "tests/bracket_tests/samples/missing_square_bracket_after_error.py"
        expected_message = get_formatted_message("missing_brackets.square.closing", count=1, line=5)
        run_test_scenario(self, missing_square_bracket_after_path, 1, expected_message)

    def test_missing_square_bracket_after2(self):
        missing_square_bracket_after_path = "tests/bracket_tests/samples/missing_square_bracket_after2_error.py"
        expected_message = get_formatted_message("missing_brackets.square.closing", count=1, line=5)
        run_test_scenario(self, missing_square_bracket_after_path, 1, expected_message)


if __name__ == '__main__':
    unittest.main()
