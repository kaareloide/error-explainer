import unittest
from test.test_utils import run_test_scenario
from error_explainer.messages import get_formatted_message


class ColonTest(unittest.TestCase):
    def test_missing_colon_after_if(self):
        path = "colon_samples/missing_colon_after_if_error.py"
        expected_message = get_formatted_message(
            "missing_colon", line_end=3, statement="if"
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_colon_after_while(self):
        path = "colon_samples/missing_colon_after_while_error.py"
        expected_message = get_formatted_message(
            "missing_colon", line_end=3, statement="while"
        )
        run_test_scenario(self, path, 1, expected_message)


if __name__ == "__main__":
    unittest.main()
