import unittest
from error_explainer.messages import get_formatted_message
from test.test_utils import run_test_scenario


class QuotesTest(unittest.TestCase):
    def test_simple_missing_single_after(self):
        path = "quotes_samples/mixed_missing_single_after.py"
        expected_message = get_formatted_message(
            "invalid_quotes", line_start=1, quote="'", pos=10
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_double_before(self):
        path = "quotes_samples/missing_double_before.py"
        expected_message = get_formatted_message(
            "invalid_quotes", line_start=1, quote='"', pos=5
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_double_after(self):
        path = "quotes_samples/missing_double_after.py"
        expected_message = get_formatted_message(
            "invalid_quotes", line_start=1, quote='"', pos=3
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_single_before(self):
        path = "quotes_samples/missing_single_before.py"
        expected_message = get_formatted_message(
            "invalid_quotes", line_start=1, quote="'", pos=5
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_single_after(self):
        path = "quotes_samples/missing_single_after.py"
        expected_message = get_formatted_message(
            "invalid_quotes", line_start=1, quote="'", pos=3
        )
        run_test_scenario(self, path, 1, expected_message)


if __name__ == "__main__":
    unittest.main()
