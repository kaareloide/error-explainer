import unittest
from utils import find_errors_and_get_simple_messages


class BracketsTest(unittest.TestCase):

    def test_missing_bracket_after(self):
        missing_bracket_after_path = "samples/missing_bracket_after_error.py"
        expected_message = "1 missing closing bracket ')' on line 2."
        self.run_test_scenario(missing_bracket_after_path, 1, expected_message)

    def test_miss_matched_bracket_types(self):
        miss_matched_bracket_path = "samples/miss_matched_bracket_error.py"
        expected_message = "Miss matched use of brackets. Square brackets are used for arrays," \
                           " normal brackets are used for tuples function definitions and so on."
        self.run_test_scenario(miss_matched_bracket_path, 1, expected_message)

    def test_miss_matched_bracket_types_multiline(self):
        miss_matched_bracket_path_multiline = "samples/miss_matched_bracket_multiline_error.py"
        expected_message = "Miss matched use of brackets. Square brackets are used for arrays," \
                           " normal brackets are used for tuples function definitions and so on."
        self.run_test_scenario(miss_matched_bracket_path_multiline, 1, expected_message)

    def test_missing_brackets_print(self):
        missing_bracket_print_path = "samples/missing_brackets_print_error.py"
        expected_message = 'Missing parenthesis for print call on line 2.' \
                           ' Print is a function and should be followed by a set' \
                           ' of parenthesis as follows: print("foo")'
        self.run_test_scenario(missing_bracket_print_path, 1, expected_message)

    def test_missing_square_bracket_after(self):
        missing_square_bracket_after_path = "samples/missing_square_bracket_after_error.py"
        expected_message = "1 missing closing bracket ']' on line 5."
        self.run_test_scenario(missing_square_bracket_after_path, 1, expected_message)

    def test_missing_square_bracket_after2(self):
        missing_square_bracket_after_path = "samples/missing_square_bracket_after2_error.py"
        expected_message = "1 missing closing bracket ']' on line 5."
        self.run_test_scenario(missing_square_bracket_after_path, 1, expected_message)

    def run_test_scenario(self, path, expected_messages_count, expected_message):
        messages = find_errors_and_get_simple_messages(path)

        # Errors found must equal expected error count
        self.assertEqual(len(messages), expected_messages_count)

        # Simple_message must be the one expected
        simple_message = messages[0][1]
        self.assertEqual(expected_message, simple_message)

if __name__ == '__main__':
    unittest.main()
