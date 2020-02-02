"""
Different checks for finding possible errors.
"""
from colon_statements import *
import utils


def count_brackets(string):
    brackets_normal = 0
    brackets_square = 0
    brackets_curly = 0
    stack = list(string)
    while stack:
        current = stack.pop(0)
        if current == "(":
            brackets_normal += 1
        elif current == ")":
            brackets_normal -= 1
        elif current == "[":
            brackets_square += 1
        elif current == "]":
            brackets_square -= 1
        elif current == "{":
            brackets_curly += 1
        elif current == "}":
            brackets_curly -= 1
    return [brackets_normal, brackets_square, brackets_curly]


def check_missing_brackets(error_node):
    """
    :param error_node: parso error node
    :return: array in the shape of [brackets_normal, brackets_square, brackets_curly] where each
    value is 0 if there are no missing brackets of that type and positive or negative depending on if there were more
    opening or closing brackets.
    """
    error_code = error_node.get_code()
    error_code = error_code.strip()
    return count_brackets(error_code)


def check_print_missing_brackets(error_node):
    """
    :param error_node: parso error node
    :return: True if print is not followed by parenthesis
    """
    error_code = error_node.get_code()
    error_code = error_code.strip()
    if error_code == "print":
        return True
    return False


def check_missing_colon(error_node):
    """
    Uses colon_statements to determine if there is a missing
     colon after a statement that should be followed by one.
    :param error_node: parso error node
    :return: the statement missing a colon or None if no colon error found
    """
    error_code = error_node.get_code()
    error_code = error_code.strip()

    for statement in colon_statements:
        if statement in error_code and ":" not in error_code:
            return statement
    return None


def check_invalid_function_def(error_node):
    error_code = error_node.get_code()
    error_code = error_code.strip()
    return error_code == "def"


def check_missing_function_def_parts(line):
    line = line.strip()
    parts = line.split(" ")
    print(parts)
    if len(parts) < 2:
        # todo figure out check for invalid name and args part
        return line
    else:
        return None


def check_invalid_function_name(line):
    line = line.strip()
    parts = line.split(" ")
    print(parts)
    if len(parts) > 1:
        should_be_variable_name = parts[1]
        should_be_variable_name = should_be_variable_name.split("(")[0]
        print(should_be_variable_name)
        if utils.is_correct_variable_name(should_be_variable_name):
            return None
        else:
            return should_be_variable_name


def check_miss_matched_bracket_type(path):
    file_as_string = utils.read_file(path)
    brackets_count = count_brackets(file_as_string)
    normal_brackets_are_equal = brackets_count[0] % 2 == 0
    square_brackets_are_equal = brackets_count[1] % 2 == 0
    curly_brackets_are_equal = brackets_count[2] % 2 == 0

    if not normal_brackets_are_equal and not square_brackets_are_equal:
        return 1
    elif not normal_brackets_are_equal and not curly_brackets_are_equal:
        return 2
    elif not curly_brackets_are_equal and not square_brackets_are_equal:
        return 3
    return 0