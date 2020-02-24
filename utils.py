import keyword
import os
from io import StringIO
import tokenize
from colon_statements import colon_statements

from simple_message_creator import SimpleMessageCreator
from search_utils import *


def find_errors_and_get_simple_messages(path):
    simple_message_creator = SimpleMessageCreator()
    filename = os.path.abspath(path)
    grammar = parso.load_grammar()
    module = grammar.parse(read_file(filename))

    found_errors = find_nodes_of_type(module.get_root_node(), parso.python.tree.PythonErrorNode)
    print(f"Found errors: {found_errors}")
    # print(found_errors[0].get_code())
    simple_message = simple_message_creator.get_simple_error_messages(module.get_root_node(), filename)
    print(f"Simple message: {simple_message}")
    return simple_message


def read_lines(path):
    with open(path, "r") as input_file:
        return input_file.readlines()


def read_file(path):
    with open(path, "r") as input_file:
        return input_file.read()


def is_correct_variable_name(string):
    print(string.isidentifier())
    return string.isidentifier() and not keyword.iskeyword(string)


def get_lines(path, lines):
    """
    Return specified lines from a file
    :param path: path to file
    :param lines: list of line numbers wanted
    :return: lines specified by line numbers
    """
    with open(path, "r") as file:
        return [x for i, x in enumerate(file) if i in lines]


def get_line(path, line):
    return get_lines(path, [line])[0]


def tokenize_line(line):
    tokens = []
    try:
        for token in tokenize.generate_tokens(StringIO(line).readline):
            tokens.append(token)
    except tokenize.TokenError:
        pass
    return tokens


def find_indentation_lines(path):
    lines = read_lines(path)
    line_number = 0
    found_lines = []
    for line in lines:
        if is_colon_statement_line(line):
            found_lines.append((line_number, line))
        line_number += 1
    return found_lines


def is_colon_statement_line(line):
    return any(statement in line for statement in list(colon_statements.keys())) and ":" in line


def count_leading_spaces(string):
    return len(string) - len(string.lstrip(" "))


def is_only_comment_line(line):
    if line[count_leading_spaces(line)] == "#":
        return True
    return False
