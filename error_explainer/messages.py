from typing import Any, NoReturn

_messages = {
    "missing_brackets.normal.closing": 'It looks like there are missing closing bracket(s) ")" ({count}) '
    "beginning on line {line_start} and ending on line {line_end}.",
    "missing_brackets.normal.opening": 'It looks like there are missing opening bracket(s) "(" ({count}) '
    "beginning on line {line_start} and ending on line {line_end}.",
    "missing_brackets.square.closing": 'It looks like there are missing closing square bracket(s) "]" ({count}) '
    "beginning on line {line_start} and ending on line {line_end}.",
    "missing_brackets.square.opening": 'It looks like there are missing opening square bracket(s) "[" ({count}) '
    "beginning on line {line_start} and ending on line {line_end}.",
    "missing_brackets.curly.closing": 'It looks like there are missing closing curly bracket(s) "}" ({count}) '
    "beginning on line {line_start} and ending on line {line_end}.",
    "missing_brackets.curly.opening": 'It looks like there are missing opening curly bracket(s) "{" ({count}) '
    "beginning on line {line_start} and ending on line {line_end}.",
    "missing_brackets.print": "It looks like you forgot the brackets after a print call on line {line_start},\n"
    " print is a function and should be followed by a set of brackets"
    ' as follows: print("foo")',
    "missing_colon": "It looks like you forgot to add a colon after a compound statement on line {line_end}.\n"
    " {statement} statements start a new indented compound statement block"
    " and should be followed by a colon.",
    "miss_matched_brackets.square.normal": "It looks like there is a mix of square and regular brackets used "
    "beginning on line {line_start} and ending on line {line_end}\n"
    "Square brackets are used for list definitions as well as getting elements "
    "from a collection or string.\n"
    "Regular brackets are used for tuple definitions function definitions "
    "and defining the order of operations in an expression.",
    "miss_matched_brackets.curly.normal": "It looks like there is a mix of curly and regular brackets used beginning"
    " on line {line_start} and ending on line {line_end}\n"
    "Curly brackets are used for map definitions and f-string templates.\n"
    "Regular brackets are used for tuple definitions function definitions"
    " and defining the order of operations in an expression.",
    "miss_matched_brackets.curly.square": "It looks like there is a mix of curly and square brackets used beginning"
    " on line {line_start} and ending on line {line_end}\n"
    "Curly brackets are used for map definitions and f-string templates.\n"
    "Square brackets are used for list definitions as well as getting elements "
    "from a collection or string.\n",
    "invalid_function_name": "It looks like there is an invalid function name on line {line_end}.\n"
    '"{invalid_name}" can not be used as a function name, because it does not match the '
    "proper naming scheme or is a reserved keyword in Python.",
    "invalid_function_name.assign_to_def": 'It looks like you tried to assign a value to the keyword "def" '
    "on line {line_end}.\n "
    '"def" is a reserved keyword used for function definitions. ',
    "missing_function_parts": 'It looks like there are missing parts in the function definition "{invalid_def}"'
    " beginning on line {line_start} and ending on line {line_end}\n"
    "Function definition should be in the form of:\n "
    '"def function_name(argument1, argument2, ...):"',
    "invalid_function_bracket": "There is a bracket right after def on line {line_end}. \n"
    '"def" should be followed by the name of the function.',
    "invalid_indentation.1": 'There is an error in the indentation on line number {line} ("{error_line}"). '
    "The line has a higher level of indentation but a new matching indentation block "
    'was newer started.',
    "invalid_indentation.2": 'There is an error in the indentation on line number {line} ("{error_line}"). '
    "The indentation of the line does not match any outer level of indentation.",
    "invalid_indentation.3": 'There is an error in the indentation on line number {line} ("{error_line}"). '
    "The line starts a new indentation block at the end of the file.",
    "invalid_indentation.4": 'There is an error in the indentation on line number {line} ("{error_line}"). '
    "No new indentation started after a statement, "
    'that should start a new block ("{last_start_of_block}").',
    "invalid_assignment": 'Invalid assignment "{statement}" beginning on line {line_start} '
    "and ending on line {line_end}\n"
    "Assignments should be in the format of variable_name,variable_name,... = expression",
    "invalid_quotes": "There is a missing {quote} that should match the one on line {line_start} at position {pos}.",
    "miss_matched_quotes": "There is a mix of single and double quotes used from line {line_start} to line {line_end}",
    "invalid_quotes_triple": "There are missing triple quotes {quote} that should match the ones on line {line_start} "
    "at position {pos}.",
    "missing_docstring_quotes": "There seem to be some missing quotes at the end of the docstring starting "
    "on line {line_start}",
    "coma_instead_of_period": "It looks like you might have used a coma instead of a period while writing a fraction "
    "on line {line_start}",
}


def get_formatted_message(message_code: str, **namespace: Any) -> str:
    """
    Get a message that corresponds to a code in the messages map
    :param message_code: code for the message
    :param namespace: kwargs for variables in the message
    :return: message corresponding to the code with arguments inserted
    """
    return _messages.get(message_code).format(**namespace)


def add_message(message_code: str, message_text: str) -> NoReturn:
    """
    Add a new message to the list of possible error explanations,
    if message for code already exists, KeyError will be raised
    :param message_code: code used as a key to later get the message
    :param message_text: explanation message text custom variable can be inserted using curly brackets
    """
    if message_code not in _messages.keys():
        _messages[message_code] = message_text
    else:
        raise KeyError(f'Message for code "{message_code}" already exists')


def remove_message(message_code: str) -> NoReturn:
    """
    Remove message from possible explanations, if matching code was not found KeyError will be raised
    :param message_code: code for the message to be removed
    """
    if _messages.pop(message_code, None) is None:
        raise KeyError(f'Message for code "{message_code}" not found')


def overwrite_message(message_code: str, message_text: str) -> NoReturn:
    """
    Overwrite a message for the given code, if matching code was not found KeyError will be raised
    :param message_code: code used as a key for the message to be overwritten
    :param message_text: explanation message text custom variable can be inserted using curly brackets
    :return:
    """
    if message_code in _messages.keys():
        _messages[message_code] = message_text
    else:
        raise KeyError(f'Message for code "{message_code}" not found')
