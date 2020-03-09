from typing import NoReturn, Any

import parso

from checks import check_quote_error, check_invalid_function_def, check_invalid_function_name, \
    check_missing_function_def_parts, check_missing_brackets, check_miss_matched_bracket_type
from messages import get_formatted_message
from search_utils import get_line_location_start, get_location_on_line, get_line_location_end
from utils import get_root_node, find_error_nodes, get_lines, tokenize_line

checks = []
messages = []


def add_check(func):
    checks.append(func)

    def wrapper(**kwargs):
        return func(**kwargs)

    return wrapper


def run_checks(filename):
    for c in checks:
        c(filename)
    return messages


def add_message(code: str, **namespace) -> NoReturn:
    """
    Add an error message to the list of found messages
    :param code: Code representing the type of error in messages.py
    :param namespace: context specific parameters to add to the error message,
     must be defined in the message found in messages.py
    """
    messages.append(get_formatted_message(code, **namespace))


@add_check
def quote_errors_check(filename):
    root_node = get_root_node(filename)
    results = check_quote_error(root_node)
    if results is not None:
        for res in results:
            add_message("invalid_quotes",
                        quote=res.get_code(),
                        line=get_line_location_start(res),
                        pos=get_location_on_line(res))


@add_check
def indentation_errors_check(filename):
    found_errors = find_error_nodes(filename)
    if len(found_errors) == 0:
        # TODO needs a lot of work
        pass
        """
        indent_check_result = check_invalid_indentation(path)
        print(f"INDENT {indent_check_result}")
        if indent_check_result is not None:
            indent_error_line_num = indent_check_result[0]
            error_line = indent_check_result[1]
            last_start_of_block = indent_check_result[2]
            indent_error_type = indent_check_result[3]
            self.add_message(indent_error_type, f"invalid_indentation.{indent_error_type.value}",
                             line=indent_error_line_num, last_start_of_block=last_start_of_block,
                             error_line=error_line)
        """


@add_check
def invalid_function_def_check(filename):
    found_errors = find_error_nodes(filename)
    for error in found_errors:
        line_num = get_line_location_end(error)
        if check_invalid_function_def(error):
            error_line = get_lines(filename, [line_num - 1])[0]
            tokens = tokenize_line(error_line)
            invalid_function_name_res = check_invalid_function_name(tokens)
            if invalid_function_name_res == "=":
                add_message("invalid_function_name.assign_to_def",
                            line=line_num)
            elif invalid_function_name_res is not None:
                add_message("invalid_function_name",
                            line=line_num,
                            invalid_name=invalid_function_name_res)
            else:
                missing_function_parts_res = check_missing_function_def_parts(error_line)
                if missing_function_parts_res is not None:
                    add_message("missing_function_parts",
                                line=line_num,
                                invalid_def=missing_function_parts_res)


@add_check
def missing_brackets_check(filename):
    found_errors = find_error_nodes(filename)
    for error in found_errors:
        line_num = get_line_location_start(error)
        normal_brackets, square_brackets, curly_brackets = check_missing_brackets(error)

        if normal_brackets + square_brackets + curly_brackets != 0:
            # If there are bracket errors check for miss matched brackets
            if check_miss_matched_bracket_type(filename) == 0:
                if normal_brackets < 0:
                    add_message("missing_brackets.normal.opening",
                                count=abs(normal_brackets),
                                line=line_num)
                elif normal_brackets > 0:
                    add_message("missing_brackets.normal.closing",
                                count=abs(normal_brackets),
                                line=line_num)
                elif square_brackets < 0:
                    add_message("missing_brackets.square.opening",
                                count=abs(square_brackets),
                                line=line_num)
                elif square_brackets > 0:
                    add_message("missing_brackets.square.closing",
                                count=abs(square_brackets),
                                line=line_num)
                elif curly_brackets < 0:
                    add_message("missing_brackets.curly.opening",
                                count=abs(curly_brackets),
                                line=line_num)
                elif curly_brackets > 0:
                    add_message("missing_brackets.curly.closing",
                                count=abs(curly_brackets),
                                line=line_num)


@add_check
def miss_matched_bracket_check(filename):
    found_errors = find_error_nodes(filename)
    for error in found_errors:
        line_num = get_line_location_start(error)
        normal_brackets, square_brackets, curly_brackets = check_missing_brackets(error)

        if normal_brackets + square_brackets + curly_brackets != 0:
            miss_matched_bracket_type_res = check_miss_matched_bracket_type(filename)
            if miss_matched_bracket_type_res == 1:
                add_message("miss_matched_brackets.square.normal",
                            line=line_num)
            elif miss_matched_bracket_type_res == 2:
                add_message("miss_matched_brackets.curly.normal",
                            line=line_num)
            elif miss_matched_bracket_type_res == 3:
                add_message("miss_matched_brackets.curly.square",
                            line=line_num)


if __name__ == '__main__':
    run_checks("tests/quotes_test/samples/simple_missing_double_after.py")
    for message in messages:
        print(message)

    print(checks)
