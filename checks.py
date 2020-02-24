"""
Different checks for finding possible errors.
"""
import tokenize

from colon_statements import *
import utils
import enum


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
    return "def" in error_code


def check_missing_function_def_parts(line):
    tokens = utils.tokenize_line(line)
    print(tokens)
    line = line.strip()
    if len(tokens) < 5:
        return line
    else:
        if not utils.is_correct_variable_name(tokens[1].string) or tokens[2].string != "(" or tokens[-2].string != ")":
            return line
    return None


def check_invalid_function_name(tokens):
    if len(tokens) > 1 and tokens[1].string == "=":
        return "="
    if len(tokens) >= 6:
        should_be_variable_name = tokens[1]
        if should_be_variable_name.type != tokenize.NAME:
            return None
        else:
            return should_be_variable_name.string


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


def check_invalid_indentation(path):
    level_stack = [0]
    statement_lines = [None]

    def is_correct_indent_level(line_to_check):
        if utils.is_only_comment_line(line_to_check):
            return True
        return utils.count_leading_spaces(line_to_check) == level_stack[0]

    def is_lower_indentation(line_to_check):
        return utils.count_leading_spaces(line_to_check) < level_stack[0]

    def get_next_non_comment_line(all_lines, from_line):
        for l in all_lines[from_line:]:
            if not utils.is_only_comment_line(l):
                return l
        return None

    lines = utils.read_lines(path)

    if utils.is_colon_statement_line(lines[len(lines) - 1]):
        # Last Line starts new indentation block
        return len(lines), lines[len(lines) - 1], lines[len(lines) - 1], IndentationErrorType.NEW_INDENT_AT_EOF
    for i, line in enumerate(lines):
        space_count = utils.count_leading_spaces(line)
        if is_correct_indent_level(line):
            # If indentation matches stack
            if utils.is_colon_statement_line(line):
                # New indentation level started.
                statement_lines.insert(0, line)
                try:
                    next_non_comment_line = get_next_non_comment_line(lines, i + 1)
                    next_indentation_level = utils.count_leading_spaces(next_non_comment_line)
                    if next_indentation_level <= level_stack[0]:
                        # If no new indent after start of block statement and is not comment line
                        return i + 1, next_non_comment_line, statement_lines[0], IndentationErrorType.NO_NEW_INDENT
                    level_stack.insert(0, next_indentation_level)
                except IndexError:
                    # New indentation started at the last line
                    return i + 1, line, statement_lines[0], IndentationErrorType.NEW_INDENT_AT_EOF

        elif is_lower_indentation(line):
            # If indentation level is lower check stack
            if space_count in level_stack:
                # If stack has that level, remove from start until that level
                index = level_stack.index(space_count) + 1
                del level_stack[0:index]
                del statement_lines[0:index]
            else:
                # If that level was not in stack, then line does not match any outer indentation level
                return i + 1, line, statement_lines[0], IndentationErrorType.DOES_NOT_MATCH_OUTER
        else:
            # Higher level of indentation without start of new block
            return i + 1, line, statement_lines[0], IndentationErrorType.HIGHER_LEVEL_WITHOUT_START


class IndentationErrorType(enum.Enum):
    HIGHER_LEVEL_WITHOUT_START = 1
    DOES_NOT_MATCH_OUTER = 2
    NEW_INDENT_AT_EOF = 3
    NO_NEW_INDENT = 4

