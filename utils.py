import keyword
import os
from simple_message_creator import get_simple_error_messages
from search_utils import *


def find_errors_and_get_simple_messages(path):
    filename = os.path.abspath(path)
    grammar = parso.load_grammar()
    module = grammar.parse(read_file(filename))
    errors = grammar.iter_errors(module)
    if len(errors) > 0:
        # Errors found
        found_errors = find_nodes_of_type(module.get_root_node(), parso.python.tree.PythonErrorNode)
        print(f"Found errors: {found_errors}")
        # print(found_errors[0].get_code())
        simple_message = get_simple_error_messages(module.get_root_node(), filename)
        print(f"Simple message: {simple_message}")
        return simple_message
    else:
        return None


def read_file(path):
    with open(path, "r") as input_file:
        return input_file.read()


def is_syntax_error(issue):
    return "SyntaxError" in issue.message


def is_correct_variable_name(string):
    print(string.isidentifier())
    return string.isidentifier() and not keyword.iskeyword(string)


def get_lines(path, lines):
    with open(path, "r") as file:
        return [x for i, x in enumerate(file) if i in lines]
