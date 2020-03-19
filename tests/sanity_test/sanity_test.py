import unittest
from temp.test_utils import run_test_scenario
from messages import get_formatted_message


class SanityTest(unittest.TestCase):
    """
    Test cases from https://wiki.python.org/moin/SimplePrograms
    """

    def test_sanity(self):
        path = "tests/sanity_test/samples/sanity.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)

    def test_sanity2(self):
        path = "tests/sanity_test/samples/sanity2.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)

    def test_sanity3(self):
        path = "tests/sanity_test/samples/sanity3.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)

    def test_sanity4(self):
        path = "tests/sanity_test/samples/sanity4.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)

    def test_sanity5(self):
        path = "tests/sanity_test/samples/sanity5.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)

    def test_sanity6(self):
        path = "tests/sanity_test/samples/sanity6.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)

    def test_sanity7(self):
        path = "tests/sanity_test/samples/sanity7.py"
        expected_message = None
        run_test_scenario(self, path, 0, expected_message)


if __name__ == '__main__':
    unittest.main()