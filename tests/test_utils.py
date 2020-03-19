from unittest import TestCase
from typing import NoReturn, List, Union

from check_runner import run_checks
from utils import find_errors_and_get_simple_messages


def run_test_scenario(test_case: TestCase, path: str, expected_messages_count: int,
                      expected_messages: Union[List[str], str, None]) -> NoReturn:
    """
    Default test scenario for checking errors in a python file.
    :param test_case: self of TestCase
    :param path: path to file
    :param expected_messages_count: number of expected messages
    :param expected_messages: 1 or more expected messages can be string or list
    :return:
    """
    messages = run_checks(path)

    # Errors found must equal expected error count
    test_case.assertEqual(len(messages), expected_messages_count)

    # Simple_message must be the one expected
    if expected_messages is not None:
        if type(expected_messages) == str:
            expected_messages = [expected_messages]
        print(messages)
        print(expected_messages)
        test_case.assertTrue(set(expected_messages) == set(messages))
