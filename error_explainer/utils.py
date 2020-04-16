import keyword
from io import StringIO
import tokenize
from tokenize import TokenInfo

import parso

from error_explainer.colon_statements import colon_statements
from typing import List, Tuple, AnyStr, Optional

from error_explainer.search_utils import find_nodes_of_type


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
    Check if string is a valid variable name and is not a reserved keyword.
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


def is_colon_statement_line(line: str) -> bool:
    """
    Check if the line contains a statement that should end with a colon.
    :param line: line to check
    :return: True/False
    """
    return (
        any(statement in line for statement in list(colon_statements.keys()))
        and ":" in line
    )


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


def is_correct_assignment_signature(code: str) -> bool:
    """
    Check if list of tokens matches the pattern of a correct assignment.
    :param code: line containing variable assignment
    :return: True/False
    """
    try:
        equals_index = code.index("=")
        if code[equals_index + 1] != "=":
            # next symbol should not be another equals sign after the first one
            should_be_var_names = code.split("=")[0]
            should_be_var_names = remove_irrelevant_tokens_in_var_names(
                tokenize_line(should_be_var_names.strip())
            )
            return should_be_var_names is None or (
                all(
                    is_correct_variable_name_token(token)
                    for token in should_be_var_names
                )
            )
    except ValueError:
        return False


def is_bad_coma_usage(code: str) -> bool:
    """
    Check if left side of the ExprStatement only has 1 variable and the right side contains a coma
    :param code:
    :return:
    """
    parts = code.split("=")

    if len(parts) != 2:
        return False

    should_be_var_names, other = code.split("=")

    if any(b in other for b in ["[", "{", "("]):
        return False

    should_be_var_names = remove_irrelevant_tokens_in_var_names(
        tokenize_line(should_be_var_names.strip())
    )
    if len(should_be_var_names) == 1:
        return any(
            token.type == tokenize.OP and token.string == ","
            for token in tokenize_line(other)
        )


def remove_irrelevant_tokens_in_var_names(
    tokens: List[tokenize.TokenInfo],
) -> Optional[List[TokenInfo]]:
    """
    remove tokens irrelevant for checking variable name correctness in an assignment and handle possible comments
    because parso recognizes comments as ExprStmt
    :param tokens: tokens that should all be variables in an assignment
    with ENDMARKER, NEWLINE "," and "." tokens included
    :return: tokens that should all be variables in an assignment
    with ENDMARKER, NEWLINE "," and "." tokens removed or None when is comment
    """
    # check for comment
    if any(token for token in tokens if token.type == tokenize.COMMENT):
        return None

    striped = [
        token
        for token in tokens
        if token.type != tokenize.ENDMARKER
        and token.type != tokenize.NEWLINE
        and token.string != ","
        and token.string != "."
    ]
    # remove last OP type token for the usage of "+=" etc
    if striped[-1].type == tokenize.OP:
        striped.remove(striped[-1])
    return striped


def is_correct_variable_name_token(token: tokenize.TokenInfo) -> bool:
    """
    Check if token is a correct variable name. Should be of type NAME and not be a reserved keyword.
    :param token: Token to check
    :return: True/False
    """
    return token.type == tokenize.NAME and is_correct_variable_name(token.string)


def get_root_node(filename: str) -> parso.python.tree.Module:
    """
    Get root Module node of a tree made by parso
    :param filename: path to python file to construct a tree from
    :return: Module node
    """
    grammar = parso.load_grammar()
    module = grammar.parse(read_file(filename))
    return module.get_root_node()


def find_error_nodes(filename: str) -> List[parso.python.tree.PythonErrorNode]:
    """
    Get error nodes of a tree made by parso
    :param filename: path to python file to construct a tree from
    :return: list of error nodes
    """
    root_node = get_root_node(filename)
    return find_nodes_of_type(root_node, parso.python.tree.PythonErrorNode)


def count_brackets(string: str) -> Tuple[int, int, int]:
    """
    Count the number of miss matched brackets
    :param string: String to count from
    :return: Tuple[normal: int, square: int, curly: int]
    """
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
    return brackets_normal, brackets_square, brackets_curly
