"""
Different checks for finding possible errors.
"""
from colon_statements import *


def check_missing_parens(error_node):
    """
    :param error_node: parso error node
    :return: 0 if no parenthesis are missing of a positive
    or negative integer based on the amount of missing parenthesis.
    """
    parens = 0
    error_code = error_node.get_code()
    error_code = error_code.strip()
    stack = list(error_code)

    while stack:
        current = stack.pop(0)
        if current == "(":
            parens += 1
        elif current == ")":
            parens -= 1
    return parens


def check_print_missing_parens(error_node):
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
