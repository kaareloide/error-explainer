import parso
from checks import *
from search_utils import *


def get_simple_error_messages(root_node):
    """
    searches for all error nodes and then runs error checks on the found nodes
    :param root_node: root node of the partial AST given by parso
    :return: list of tuples in the form of (error node, simple message) of all the found errors
    """
    messages = []
    found_errors = find_nodes_of_type(root_node, parso.python.tree.PythonErrorNode)
    for error in found_errors:
        missing_colon_result = check_missing_colon(error)
        # All error checks go here
        missing_parens_res = check_missing_parens(error)
        line_num = get_line_location(error)

        if missing_parens_res < 0:
            # missing opening paren
            messages.append((error, f"{abs(missing_parens_res)} missing opening parenthesis on line {line_num}."))
        elif missing_parens_res > 0:
            messages.append((error, f"{abs(missing_parens_res)} missing closing parenthesis on line {line_num}."))
        elif check_print_missing_parens(error):
            messages.append((error, f"Missing parenthesis for print call on line {line_num}. "
                                    f"Print is a function and should be followed by a set of parenthesis as follows: "
                                    f"print(\"foo\")"))
        elif missing_colon_result is not None:
            #todo make specific examples for statements
            messages.append((error, f"Missing colon before an indentation block on line {line_num}. "
                                    f"{missing_colon_result} statements should be followed by a colon."))

    return messages