from utils import find_errors_and_get_simple_messages


def run_test_scenario(test_case, path, expected_messages_count, expected_message):
    messages = find_errors_and_get_simple_messages(path)

    # Errors found must equal expected error count
    test_case.assertEqual(len(messages), expected_messages_count)

    # Simple_message must be the one expected
    only_messages = [message[1] for message in messages]
    print(only_messages)
    print(expected_message)
    test_case.assertTrue(expected_message in only_messages)
