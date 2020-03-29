import ast
from typing import NoReturn, Any, List, Callable

import parso

from error_explainer.checks import (
    check_quote_error,
    check_invalid_function_def,
    check_invalid_function_name,
    check_missing_function_def_parts,
    check_missing_brackets,
    check_miss_matched_bracket_type,
    check_print_missing_brackets,
    check_missing_colon,
    check_invalid_assignment_expr,
    BracketErrorType,
)
from error_explainer.messages import get_formatted_message
from error_explainer.search_utils import (
    get_line_location_start,
    get_location_on_line,
    get_line_location_end,
)
from error_explainer.utils import (
    get_root_node,
    find_error_nodes,
    get_lines,
    tokenize_line,
    read_file,
)

checks = dict()
messages = []


def add_check(func: Callable) -> Callable:
    """
    Decorator for adding a check to the list of checks to run when calling run_checks
    """
    checks[func.__name__] = func

    def wrapper(**kwargs):
        return func(**kwargs)

    return wrapper


def run_checks(filename: str) -> List[str]:
    """
    Run all checks added with add_check and return gotten messages
    :param filename: path to file to check
    :return: list of messages
    """
    global messages
    messages = []
    try:
        # check if code compiles
        ast.parse(read_file(filename))
    except Exception:
        # if not then there is a syntax error and checks need to be ran
        for c in checks.keys():
            checks.get(c)(filename)

    return messages


def add_message(code: str, **namespace: Any) -> NoReturn:
    """
    Add an error message to the list of found messages
    :param code: Code representing the type of error in messages.py
    :param namespace: context specific parameters to add to the error message,
     must be defined in the message found in messages.py
    """
    messages.append(get_formatted_message(code, **namespace))


def remove_check(name: str) -> NoReturn:
    """
    Remove a check function from the list of checks ran with run_checks()
    :param name: name of the check function to be removed
    """
    if checks.pop(name, None) is None:
        raise KeyError(f"Check with the name {name} not found")


def list_checks() -> List[str]:
    """
    List checks by name that will be ran with run_checks()
    :return: list check function names
    """
    return list(checks.keys())


@add_check
def quote_errors_check(filename: str) -> NoReturn:
    root_node = get_root_node(filename)
    results = check_quote_error(root_node)
    if results is not None:
        for res in results:
            add_message(
                "invalid_quotes",
                quote=res.get_code().strip(),
                line_start=get_line_location_start(res),
                pos=get_location_on_line(res),
            )


@add_check
def indentation_errors_check(filename: str) -> NoReturn:
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
def invalid_function_def_check(filename: str) -> NoReturn:
    found_errors = find_error_nodes(filename)
    for error in found_errors:
        if check_invalid_function_def(error):
            error_line = get_lines(filename, [get_line_location_end(error) - 1])[0]
            tokens = tokenize_line(error_line)
            invalid_function_name_res = check_invalid_function_name(tokens)
            if invalid_function_name_res == "=":
                add_message(
                    "invalid_function_name.assign_to_def",
                    line_end=get_line_location_end(error),
                )
            elif invalid_function_name_res is not None:
                if invalid_function_name_res == "(":
                    add_message(
                        "invalid_function_bracket",
                        line_end=get_line_location_end(error),
                    )
                else:
                    add_message(
                        "invalid_function_name",
                        line_end=get_line_location_end(error),
                        invalid_name=invalid_function_name_res,
                    )
            else:
                missing_function_parts_res = check_missing_function_def_parts(
                    error_line
                )
                if missing_function_parts_res is not None:
                    add_message(
                        "missing_function_parts",
                        line_start=get_line_location_start(error),
                        line_end=get_line_location_end(error),
                        invalid_def=missing_function_parts_res,
                    )


@add_check
def missing_brackets_check(filename: str) -> NoReturn:
    found_errors = find_error_nodes(filename)
    for error in found_errors:
        normal_brackets, square_brackets, curly_brackets = check_missing_brackets(error)

        if normal_brackets + square_brackets + curly_brackets != 0:
            # If there are bracket errors check for miss matched brackets
            if check_miss_matched_bracket_type(filename) is None:
                if normal_brackets < 0:
                    add_message(
                        "missing_brackets.normal.opening",
                        count=abs(normal_brackets),
                        line_start=get_line_location_start(error),
                        line_end=get_line_location_end(error),
                    )
                elif normal_brackets > 0:
                    add_message(
                        "missing_brackets.normal.closing",
                        count=abs(normal_brackets),
                        line_start=get_line_location_start(error),
                        line_end=get_line_location_end(error),
                    )
                elif square_brackets < 0:
                    add_message(
                        "missing_brackets.square.opening",
                        count=abs(square_brackets),
                        line_start=get_line_location_start(error),
                        line_end=get_line_location_end(error),
                    )
                elif square_brackets > 0:
                    add_message(
                        "missing_brackets.square.closing",
                        count=abs(square_brackets),
                        line_start=get_line_location_start(error),
                        line_end=get_line_location_end(error),
                    )
                elif curly_brackets < 0:
                    add_message(
                        "missing_brackets.curly.opening",
                        count=abs(curly_brackets),
                        line_start=get_line_location_start(error),
                        line_end=get_line_location_end(error),
                    )
                elif curly_brackets > 0:
                    add_message(
                        "missing_brackets.curly.closing",
                        count=abs(curly_brackets),
                        line_start=get_line_location_start(error),
                        line_end=get_line_location_end(error),
                    )


@add_check
def miss_matched_bracket_check(filename: str) -> NoReturn:
    found_errors = find_error_nodes(filename)
    for error in found_errors:
        normal_brackets, square_brackets, curly_brackets = check_missing_brackets(error)

        if normal_brackets + square_brackets + curly_brackets != 0:
            miss_matched_bracket_type_res = check_miss_matched_bracket_type(filename)
            if miss_matched_bracket_type_res == BracketErrorType.NORMAL_SQUARE:
                add_message(
                    "miss_matched_brackets.square.normal",
                    line_start=get_line_location_start(error),
                    line_end=get_line_location_end(error),
                )
            elif miss_matched_bracket_type_res == BracketErrorType.NORMAL_CURLY:
                add_message(
                    "miss_matched_brackets.curly.normal",
                    line_start=get_line_location_start(error),
                    line_end=get_line_location_end(error),
                )
            elif miss_matched_bracket_type_res == BracketErrorType.CURLY_SQUARE:
                add_message(
                    "miss_matched_brackets.curly.square",
                    line_start=get_line_location_start(error),
                    line_end=get_line_location_end(error),
                )


@add_check
def missing_brackets_print_check(filename: str) -> NoReturn:
    found_errors = find_error_nodes(filename)
    for error in found_errors:
        if check_print_missing_brackets(error):
            add_message(
                "missing_brackets.print", line_start=get_line_location_start(error)
            )


@add_check
def missing_colon_check(filename: str) -> NoReturn:
    def should_check_for_missing_colon(e: parso.python.tree.ErrorNode) -> bool:
        """
        Check for colon only when no bracket error or definition error is present
        """
        is_not_missing_brackets_error = sum(check_missing_brackets(e)) == 0
        def_res = check_invalid_function_def(e)
        is_not_def_error = def_res is None or not def_res
        return (
            is_not_missing_brackets_error
            and is_not_def_error
            and not check_print_missing_brackets(e)
        )

    found_errors = find_error_nodes(filename)
    for error in found_errors:
        if should_check_for_missing_colon(error):
            res = check_missing_colon(error)
            if res is not None:
                add_message(
                    "missing_colon",
                    line_end=get_line_location_end(error),
                    statement=res,
                )


@add_check
def invalid_assignment_check(filename: str) -> NoReturn:
    root_node = get_root_node(filename)
    invalid_assignment_res = check_invalid_assignment_expr(root_node)
    if invalid_assignment_res is not None and check_quote_error(root_node) is None:
        for res in invalid_assignment_res:
            add_message(
                "invalid_assignment",
                statement=res.get_code().strip(),
                line_start=get_line_location_start(res),
                line_end=get_line_location_end(res),
            )
