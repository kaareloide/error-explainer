from typing import Any

messages = {
    "missing_brackets.normal.closing": 'It looks like there are missing closing bracket(s) ")" ({count}) '
                                       'on line {line}.',
    "missing_brackets.normal.opening": 'It looks like there are missing opening bracket(s) "(" ({count}) '
                                       'on line {line}.',
    "missing_brackets.square.closing": 'It looks like there are missing closing square bracket(s) "]" ({count}) '
                                       'on line {line}.',
    "missing_brackets.square.opening": 'It looks like there are missing opening square bracket(s) "[" ({count}) '
                                       'on line {line}.',
    "missing_brackets.curly.closing":  'It looks like there are missing closing curly bracket(s) "}" ({count}) '
                                       'on line {line}.',
    "missing_brackets.curly.opening":  'It looks like there are missing opening curly bracket(s) "{" ({count}) '
                                       'on line {line}.',

    "missing_brackets.print": 'It looks like you forgot the brackets after a print call on line {line},\n'
                              ' print is a function and should be followed by a set of brackets'
                              ' as follows: print("foo")',

    "missing_colon": 'It looks like you forgot to add a colon after a compound statement on line {line}.\n'
                     ' {statement} statements start a new indented compound statement block'
                     ' and should be followed by a colon.',

    "miss_matched_brackets.square.normal": 'It looks like there is a mix of square and regular brackets used starting '
                                           'on line {line}.\n'
                                           'Square brackets are used for list definitions as well as getting elements '
                                           'from a collection or string.\n'
                                           'Regular brackets are used for tuple definitions function definitions '
                                           'and defining the order of operations in an expression.',

    "miss_matched_brackets.curly.normal":   'It looks like there is a mix of curly and regular brackets used starting '
                                            'on line {line}.\n'
                                            'Curly brackets are used for map definitions and f-string templates.\n'
                                            'Regular brackets are used for tuple definitions function definitions'
                                            ' and defining the order of operations in an expression.',

    "miss_matched_brackets.curly.square":   'It looks like there is a mix of curly and square brackets used starting '
                                            'on line {line}.\n'
                                            'Curly brackets are used for map definitions and f-string templates.\n'
                                            'Square brackets are used for list definitions as well as getting elements '
                                            'from a collection or string.\n',

    "invalid_function_name": 'It looks like there is an Invalid function name on line {line}.\n'
                             '"{invalid_name}" can not be used as a function name, because it does not match the '
                             'proper naming scheme or is a reserved keyword in Python.',

    "invalid_function_name.assign_to_def": 'It looks like you tried to assign a value to the keyword "def" '
                                           'on line {line}.\n '
                                           '"def" is a reserved keyword used for function definitions. ',

    "missing_function_parts": 'It looks like there are missing parts in the function definition "{invalid_def}" on '
                              'line {line}.\n'
                              'Function definition should be in the form of:\n '
                              '"def function_name(argument1, argument2, ...):"',

    "invalid_indentation.1": 'There is an error in the indentation on line number {line} ("{error_line}"). '
                             'The line has a higher level of indentation but a new matching indentation block '
                             'was newer started. Last start of an indentation block was "{last_start_of_block}".',

    "invalid_indentation.2": 'There is an error in the indentation on line number {line} ("{error_line}"). '
                             'The indentation of the line does not match any outer level of indentation.',

    "invalid_indentation.3": 'There is an error in the indentation on line number {line} ("{error_line}"). '
                             'The line starts a new indentation block at the end of the file.',

    "invalid_indentation.4": 'There is an error in asd the indentation on line number {line} ("{error_line}"). '
                             'No new indentation started after a statement, '
                             'that should start a new block ("{last_start_of_block}").',

    "invalid_assignment": 'Invalid assignment "{statement}" on line {line}.\n'
                          'Assignments should be in the format of variable_name = expression.',

    "invalid_quotes": 'There is a missing {quote} that should match the one on line {line} at position {pos}.'
}


def get_formatted_message(message_code: str, **namespace: Any) -> str:
    """
    Get a message that corresponds to a code in the messages map
    :param message_code: code for the message
    :param namespace: kwargs for variables in the message
    :return: message corresponding to the code with arguments inserted
    """
    return messages.get(message_code).format(**namespace)