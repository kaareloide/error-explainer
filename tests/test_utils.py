from utils import find_errors_and_get_simple_messages


def run_test_scenario(test_case, path, expected_messages_count, expected_message):
    messages = find_errors_and_get_simple_messages(path)

    # Errors found must equal expected error count
    test_case.assertEqual(len(messages), expected_messages_count)

    # Simple_message must be the one expected
    simple_message = messages[0][1]
    test_case.assertEqual(expected_message, simple_message)
