import unittest
from ..test_utils import run_test_scenario
from messages import get_formatted_message


class ColonTest(unittest.TestCase):

    def test_missing_colon_after_if(self):
        missing_colon_after_if_path = "tests/colon_tests/samples/missing_colon_after_if_error.py"
        expected_message = get_formatted_message("missing_colon", line=2, statement="if")
        run_test_scenario(self, missing_colon_after_if_path, 1, expected_message)

    def test_missing_colon_after_while(self):
        missing_colon_after_if_path = "tests/colon_tests/samples/missing_colon_after_while_error.py"
        expected_message = get_formatted_message("missing_colon", line=2, statement="while")
        run_test_scenario(self, missing_colon_after_if_path, 1, expected_message)


if __name__ == '__main__':
    unittest.main()
