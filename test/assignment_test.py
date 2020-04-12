import unittest
from test.test_utils import run_test_scenario, run_sanity_test
from error_explainer.messages import get_formatted_message


class AssignmentTest(unittest.TestCase):
    def test_assignment_to_keyword(self):
        path = "assignment_samples/assignment_to_keyword_error.py"
        expected_message = get_formatted_message(
            "invalid_assignment", statement="None = 1", line_start=1, line_end=1
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_assignment_to_function(self):
        path = "assignment_samples/assignment_to_function_error.py"
        expected_message = get_formatted_message(
            "invalid_assignment", statement="f() = 1", line_start=3, line_end=4
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_assignment_to_expr(self):
        path = "assignment_samples/assignment_to_expr_error.py"
        expected_message = get_formatted_message(
            "invalid_assignment", statement="a + 1 = 2", line_start=1, line_end=1
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_assignment_to_variable_1(self):
        path = "assignment_samples/assignment_to_variable_error_1.py"
        expected_message = get_formatted_message(
            "invalid_assignment", statement='"abc" = 1', line_start=1, line_end=1
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_assignment_to_variable_2(self):
        path = "assignment_samples/assignment_to_variable_error_2.py"
        expected_message = get_formatted_message(
            "invalid_assignment", statement="3 = 1", line_start=1, line_end=1
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_assignment_to_variable_3(self):
        path = "assignment_samples/assignment_to_variable_error_3.py"
        expected_message = get_formatted_message(
            "invalid_assignment", statement="True = 1", line_start=1, line_end=1
        )
        run_test_scenario(self, path, 1, expected_message)

    def test_multiple(self):
        path = "assignment_samples/multiple_assignment_func_var_error.py"
        expected_messages = [
            get_formatted_message(
                "invalid_assignment", statement="True = 1", line_start=1, line_end=1
            ),
            get_formatted_message(
                "invalid_assignment", statement="f() = 1", line_start=5, line_end=6
            ),
        ]
        run_test_scenario(self, path, 2, expected_messages)

    def test_comparison_assignment(self):
        run_sanity_test(self, "assignment_samples/comparison_assignment_correct.py")

    def test_tuple_assignment(self):
        run_sanity_test(self, "assignment_samples/tuple_assign_correct.py")

    def test_coma_instead_of_period(self):
        path = "assignment_samples/coma_instead_of_period_error.py"
        expected_message = get_formatted_message("coma_instead_of_period", line_start=1)
        run_test_scenario(self, path, 1, expected_message)


if __name__ == "__main__":
    unittest.main()
