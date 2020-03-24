import unittest

from test.test_utils import run_sanity_test


class SanityTest(unittest.TestCase):
    """
    Test cases from https://wiki.python.org/moin/SimplePrograms
    there is a bracket error at the start of every file to get past
    ast.parse() check, the premise of these asd is to only detect
    that firs error and not any other false positives
    """

    def test_sanity(self):
        run_sanity_test(self, "sanity_samples/sanity.py")

    def test_sanity2(self):
        run_sanity_test(self, "sanity_samples/sanity2.py")

    def test_sanity3(self):
        run_sanity_test(self, "sanity_samples/sanity3.py")

    def test_sanity4(self):
        run_sanity_test(self, "sanity_samples/sanity4.py")

    def test_sanity5(self):
        run_sanity_test(self, "sanity_samples/sanity5.py")

    def test_sanity6(self):
        run_sanity_test(self, "sanity_samples/sanity6.py")

    def test_sanity7(self):
        run_sanity_test(self, "sanity_samples/sanity7.py")


if __name__ == "__main__":
    unittest.main()
