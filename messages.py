messages = {
    "missing_brackets.normal.closing": f"{{count}} missing closing bracket ')' on line {{line}}.",
    "missing_brackets.normal.opening": f"{{count}} missing opening bracket '(' on line {{line}}.",
    "missing_brackets.square.closing": f"{{count}} missing closing bracket ']' on line {{line}}.",
    "missing_brackets.square.opening": f"{{count}} missing opening bracket '[' on line {{line}}.",
    "missing_brackets.curly.closing": f"{{count}} missing closing bracket '}}' on line {{line}}.",
    "missing_brackets.curly.opening": f"{{count}} missing opening bracket '{{' on line {{line}}.",

    "missing_brackets.print": f'Missing parenthesis for print call on line {{line}}.'
                              f' Print is a function and should be followed by a set of parenthesis'
                              f' as follows: print("foo")',

    "missing_colon": f"Missing colon before an indentation block on line {{line}}."
                     f" {{statement}} statements should be followed by a colon.",

    "miss_matched_brackets.square.normal": f"Miss matched use of brackets starting on line {{line}}. "
                                           f"Square brackets are used for lists,"
                                           f" normal brackets are used for tuples function definitions and so on.",

    "miss_matched_brackets.curly.normal": f"Miss matched use of brackets starting on line {{line}}. "
                                          f"Curly brackets are used for maps and f-strings,"
                                          f" normal brackets are used for tuples function definitions and so on.",

    "miss_matched_brackets.curly.square": f"Miss matched use of brackets starting on line {{line}}. "
                                          f"Curly brackets are used for maps and f-strings, "
                                          f"square brackets are used for lists.",

    "invalid_function_name": f'Invalid function name on line {{line}}. '
                             f'"{{invalid_name}}" can not be used as a function name, '
                             f'because it does not match the proper naming scheme or is a reserved keyword.',

    "invalid_function_name.assign_to_def": f'"def" keyword on line {{line}} is used for function definitions. '
                                           f'Cannot assign a value to "def" keyword.',

    "missing_function_parts": f'There are missing parts in the function definition "{{invalid_def}}" on line {{line}}. '
                              f'Function definition should be in the form of '
                              f'"def function_name(argument1, argument2, ...):',

    "invalid_indentation.1": f'There is an error in the indentation on line number {{line}} ("{{error_line}}"). '
                             f'The line has a higher level of indentation but a new matching indentation block '
                             f'was newer started. Last start of an indentation block was "{{last_start_of_block}}".',

    "invalid_indentation.2": f'There is an error in the indentation on line number {{line}} ("{{error_line}}"). '
                             f'The indentation of the line does not match any outer level of indentation.',

    "invalid_indentation.3": f'There is an error in the indentation on line number {{line}} ("{{error_line}}"). '
                             f'The line starts a new indentation block at the end of the file.',

    "invalid_indentation.4": f'There is an error in the indentation on line number {{line}} ("{{error_line}}"). '
                             f'No new indentation started after a statement, '
                             f'that should start a new block ("{{last_start_of_block}}").',

    "invalid_assignment": f'Invalid assignment "{{statement}}" on line {{line}}. '
                          f'Assignments should be in the format of variable_name = expression.',

    "invalid_quotes": f'There is a missing {{quote}} that should match the one on line {{line}} at position {{pos}}.'
}


def get_formatted_message(message_code: str, **namespace) -> str:
    return messages.get(message_code).format(**namespace)
