messages = {
    "missing_brackets.normal.closing": "{count} missing closing bracket ')' on line {line}.",
    "missing_brackets.normal.opening": "{count} missing opening bracket '(' on line {line}.",
    "missing_brackets.square.closing": "{count} missing closing bracket ']' on line {line}.",
    "missing_brackets.square.opening": "{count} missing opening bracket '[' on line {line}.",
    "missing_brackets.curly.closing": "{count} missing closing bracket '}' on line {line}.",
    "missing_brackets.curly.opening": "{count} missing opening bracket '{' on line {line}.",
    "missing_brackets.print": 'Missing parenthesis for print call on line {line}. Print is a function and should be followed by a set of parenthesis as follows: print("foo")',
    "missing_colon": "Missing colon before an indentation block on line {line}. {statement} statements should be followed by a colon.",
    "miss_matched_brackets.square.normal": "Miss matched use of brackets starting on line {line}. Square brackets are used for lists, normal brackets are used for tuples function definitions and so on.",
    "miss_matched_brackets.curly.normal": "Miss matched use of brackets starting on line {line}. Curly brackets are used for maps and f-strings, normal brackets are used for tuples function definitions and so on.",
    "miss_matched_brackets.curly.square": "Miss matched use of brackets starting on line {line}. Curly brackets are used for maps and f-strings, Square brackets are used for lists.",
    "invalid_function_name": 'Invalid function name on line {line}. "{invalid_name}" can not be used as a function name, because it does not match the proper naming scheme or is a reserved keyword.',
    "invalid_function_name.assign_to_def": '"def" keyword on line {line} is used for function definitions. Cannot assign a value to "def" keyword.',
    "missing_function_parts": 'There are missing parts in the function definition "{invalid_def}" on line {line}. Function definition should be in the form of "def function_name(argument1, argument2, ...):',
    "invalid_indentation.1": 'There is an error in the indentation on line number {line} ("{error_line}"). The line has a higher level of indentation but a new matching indentation block was newer started. Last start of an indentation block was "{last_start_of_block}".',
    "invalid_indentation.2": 'There is an error in the indentation on line number {line} ("{error_line}"). The indentation of the line does not match any outer level of indentation.',
    "invalid_indentation.3": 'There is an error in the indentation on line number {line} ("{error_line}"). The line starts a new indentation block at the end of the file.',
    "invalid_indentation.4": 'There is an error in the indentation on line number {line} ("{error_line}"). No new indentation started after a statement, that should start a new block ("{last_start_of_block}").',
}


def get_formatted_message(message_code, **namespace):
    return messages.get(message_code).format(**namespace)
