import keyword
import os
from io import StringIO
import tokenize
from tokenize import TokenInfo
from colon_statements import colon_statements
from typing import List, Tuple, AnyStr, Any

from simple_message_creator import SimpleMessageCreator
from search_utils import *


def find_errors_and_get_simple_messages(path: str) -> List[Tuple[Any, AnyStr]]:
    """
    TODO refactor
    Returns simple messages found by SimpleMessageCreator.
    :param path: path to file
    :return: list of tuples containing error and new message
    """
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


def read_lines(path: str) -> List[AnyStr]:
    """
    Read whole file as a list of lines
    :param path: path to file
    :return: file content as a list of lines
    """
    with open(path, "r") as input_file:
        return input_file.readlines()


def read_file(path: str) -> AnyStr:
    """
    Read whole file as a string.
    :param path: path to file
    :return: file content as a string
    """
    with open(path, "r") as input_file:
        return input_file.read()


def is_correct_variable_name(string: str) -> bool:
    """
    Check if string is a valid variable name.
    :param string: string to check
    :return: True/False
    """
    return string.isidentifier() and not keyword.iskeyword(string)


def get_lines(path: str, lines: List[int]) -> List[str]:
    """
    Return specified lines from a file.
    :param path: path to file
    :param lines: list of line numbers wanted
    :return: lines specified by line numbers as strings
    """
    with open(path, "r") as file:
        return [x for i, x in enumerate(file) if i in lines]


def get_line(path: str, line: int) -> str:
    """
    Gets a line from a file by line number.
    :param path: path to file
    :param line: line number
    :return: line from file as a string
    """
    return get_lines(path, [line])[0]


def tokenize_line(line: str) -> List[TokenInfo]:
    """
    Tokenizes line.
    :param line: line to tokenize
    :return: List of TokenInfo
    """
    tokens = []
    try:
        for token in tokenize.generate_tokens(StringIO(line).readline):
            tokens.append(token)
    except tokenize.TokenError:
        pass
    return tokens


def find_colon_lines(path: str) -> List[Tuple[int, str]]:
    """
    Find all lines containing a statement that should end with a colon.
    :param path: path to file
    :return: List[Tuple[int, str]] where int is line number and str is line
    """
    lines = read_lines(path)
    line_number = 0
    found_lines = []
    for line in lines:
        if is_colon_statement_line(line):
            found_lines.append((line_number, line))
        line_number += 1
    return found_lines


def is_colon_statement_line(line: str) -> bool:
    """
    Check if the line contains a statement that should end with a colon.
    :param line: line to check
    :return: True/False
    """
    return any(statement in line for statement in list(colon_statements.keys())) and ":" in line


def count_leading_spaces(string: str) -> int:
    """
    Count the number of spaces in a string before any other character.
    :param string: input string
    :return: number of spaces
    """
    return len(string) - len(string.lstrip(" "))


def is_only_comment_line(line: str) -> bool:
    """
    Check if the given line only consists of a comment that starts with a #.
    :param line: line to check
    :return: True/False
    """
    if line[count_leading_spaces(line)] == "#":
        return True
    return False
