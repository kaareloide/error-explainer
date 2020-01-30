import parso
from checks import *
from search_utils import *
import utils


def get_simple_error_messages(root_node, path):
    """
    searches for all error nodes and then runs error checks on the found nodes
    :param root_node: root node of the partial AST given by parso
    :param path path to the python file
    :return: list of tuples in the form of (error node, simple message) of all the found errors
    """
    messages = []
    found_errors = find_nodes_of_type(root_node, parso.python.tree.PythonErrorNode)
    for error in found_errors:
        missing_colon_result = None
        line_num = get_line_location(error)
        if check_invalid_function_def(error):
            invalid_function_name_res = check_invalid_function_name(utils.get_lines(path, [get_line_location(error)])[0])
            print(invalid_function_name_res)
            if invalid_function_name_res is not None:
                messages.append((error, f"On line {line_num} '{invalid_function_name_res}' can not be used as a function name, because it "
                                        f"does not match the proper naming scheme or is a reserved keyword."))
            else:
                missing_colon_result = check_missing_colon(error)
        # All error checks go here
        missing_brackets_res = check_missing_brackets(error)
        missing_normal_brackets_res = missing_brackets_res[0]
        missing_square_brackets_res = missing_brackets_res[1]
        missing_curly_brackets_res = missing_brackets_res[2]

        if sum(missing_brackets_res) != 0:
            # If there are bracket errors check for miss matched brackets
            miss_matched_bracket_type_res = check_miss_matched_bracket_type(path)
            if miss_matched_bracket_type_res == 1:
                messages.append(
                    (error, f"Miss matched use of brackets. Square brackets are used for arrays, normal brackets "
                            f"are used for tuples function definitions and so on."))
            elif miss_matched_bracket_type_res == 2:
                messages.append(
                    (error, f"Miss matched use of brackets. Curly brackets are used for maps and f-strings,"
                            f" normal brackets are used for tuples function definitions and so on."))
            elif miss_matched_bracket_type_res == 3:
                messages.append(
                    (error, f"Miss matched use of brackets. Curly brackets are used for maps and f-strings,"
                            f" Square brackets are used for arrays."))
            else:
                if missing_normal_brackets_res < 0:
                    # missing opening paren
                    messages.append(
                        (error, f"{abs(missing_normal_brackets_res)} missing opening bracket '(' on line {line_num}."))
                elif missing_normal_brackets_res > 0:
                    messages.append(
                        (error, f"{abs(missing_normal_brackets_res)} missing closing bracket ')' on line {line_num}."))
                elif missing_square_brackets_res < 0:
                    messages.append(
                        (error, f"{abs(missing_square_brackets_res)} missing closing bracket '[' on line {line_num}."))
                elif missing_square_brackets_res > 0:
                    messages.append(
                        (error, f"{abs(missing_square_brackets_res)} missing closing bracket ']' on line {line_num}."))
                elif missing_curly_brackets_res < 0:
                    messages.append(
                        (error, f"{abs(missing_curly_brackets_res)} missing closing bracket '{{' on line {line_num}."))
                elif missing_curly_brackets_res > 0:
                    messages.append(
                        (error, f"{abs(missing_curly_brackets_res)} missing closing bracket '}}' on line {line_num}."))

        if check_print_missing_brackets(error):
            messages.append((error, f"Missing parenthesis for print call on line {line_num}. "
                                    f"Print is a function and should be followed by a set of parenthesis as follows: "
                                    f"print(\"foo\")"))
        elif missing_colon_result is not None:
            #todo make specific examples for statements
            messages.append((error, f"Missing colon before an indentation block on line {line_num}. "
                                    f"{missing_colon_result} statements should be followed by a colon."))

    return messages