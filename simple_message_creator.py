from checks import *
from search_utils import *
import utils
from messages import get_formatted_message
from typing import Any, NoReturn


class SimpleMessageCreator(object):
    """
    Main class for finding errors and creating simple error messages
    """
    def __init__(self):
        self.messages = []
        self.missing_brackets_res = None
        self.invalid_function_def_res = None


    def get_simple_error_messages(self, root_node: parso.python.tree.Module, path: str) -> List[Tuple[Any, str]]:
        """
        Main function that checks for possible syntax errors.
        :param root_node: root node of the partial AST given by Parso
        :param path Path to file
        :return: List of all found errors in the form of tuples (error, simple message)
        """

        found_errors = find_nodes_of_type(root_node, parso.python.tree.PythonErrorNode)
        # invalid_assignment_res = check_invalid_assignment_expr(root_node)
        invalid_assignment_res = []
        print(f"invalid_assignment_res{invalid_assignment_res}")
        quote_check_res = check_quote_error(root_node)
        if quote_check_res is not None:
            for res in quote_check_res:
                self.add_message(res, "invalid_quotes",
                                 quote=res.get_code(), line=get_line_location_start(res), pos=get_location_on_line(res))
        elif len(invalid_assignment_res) > 0:
            for res in invalid_assignment_res:
                self.add_message(res, "invalid_assignment",
                                 statement=res.get_code().strip(), line=get_line_location_end(res))
        else:
            if len(found_errors) == 0:
                self.run_indent_check(path)
            for error in found_errors:
                line_num = get_line_location_end(error)
                missing_colon_result = None
                self.run_check_invalid_function_def(error, path)
                self.run_missing_brackets_checks(error, path)

                if sum(self.missing_brackets_res) == 0 and self.is_not_def_error():
                    missing_colon_result = check_missing_colon(error)
                    if missing_colon_result is None:
                        self.run_indent_check(path)

                if check_print_missing_brackets(error):
                    self.add_message(error, "missing_brackets.print", line=line_num)
                elif missing_colon_result is not None:
                    self.add_message(error, "missing_colon", line=line_num, statement=missing_colon_result)

        return self.messages

    #######
    #
    # Checks
    #
    #######

    def run_check_invalid_function_def(self, error: parso.python.tree.PythonErrorNode, path: str) -> NoReturn:
        """
        Run a check to see if the found PythonErrorNode is a definition error
        and add simple message according to the response of the check.
        :param error: Parso PythonErrorNode
        :param path: Path to file
        """

        line_num = utils.get_line_location_end(error)

        self.invalid_function_def_res = check_invalid_function_def(error)
        if self.invalid_function_def_res:
            error_line = utils.get_lines(path, [line_num-1])[0]
            tokens = utils.tokenize_line(error_line)
            invalid_function_name_res = check_invalid_function_name(tokens)
            if invalid_function_name_res == "=":
                self.add_message(error, "invalid_function_name.assign_to_def", line=line_num)
            elif invalid_function_name_res is not None:
                self.add_message(error, "invalid_function_name",
                                 line=line_num, invalid_name=invalid_function_name_res)
            else:
                missing_function_parts_res = check_missing_function_def_parts(error_line)
                if missing_function_parts_res is not None:
                    self.add_message(error, "missing_function_parts",
                                     line=line_num, invalid_def=missing_function_parts_res)

    def run_missing_brackets_checks(self, error: parso.python.tree.PythonErrorNode, path: str) -> NoReturn:
        """
        Run a check to see if the found PythonErrorNode is a missing brackets error
        and add simple message according to the response of the check.
        :param error: Parso PythonErrorNode
        :param path: Path to file
        """
        line_num = get_line_location_start(error)
        self.missing_brackets_res = check_missing_brackets(error)
        missing_normal_brackets_res = self.missing_brackets_res[0]
        missing_square_brackets_res = self.missing_brackets_res[1]
        missing_curly_brackets_res = self.missing_brackets_res[2]

        if sum(self.missing_brackets_res) != 0:
            # If there are bracket errors check for miss matched brackets
            miss_matched_bracket_type_res = check_miss_matched_bracket_type(path)
            if miss_matched_bracket_type_res == 1:
                self.add_message(error, "miss_matched_brackets.square.normal", line=line_num)
            elif miss_matched_bracket_type_res == 2:
                self.add_message(error, "miss_matched_brackets.curly.normal", line=line_num)
            elif miss_matched_bracket_type_res == 3:
                self.add_message(error, "miss_matched_brackets.curly.square", line=line_num)
            else:
                if missing_normal_brackets_res < 0:
                    self.add_message(error, "missing_brackets.normal.opening",
                                     count=abs(missing_normal_brackets_res), line=line_num)
                elif missing_normal_brackets_res > 0:
                    self.add_message(error, "missing_brackets.normal.closing",
                                     count=abs(missing_normal_brackets_res), line=line_num)
                elif missing_square_brackets_res < 0:
                    self.add_message(error, "missing_brackets.square.opening",
                                     count=abs(missing_square_brackets_res), line=line_num)
                elif missing_square_brackets_res > 0:
                    self.add_message(error, "missing_brackets.square.closing",
                                     count=abs(missing_square_brackets_res), line=line_num)
                elif missing_curly_brackets_res < 0:
                    self.add_message(error, "missing_brackets.curly.opening",
                                     count=abs(missing_curly_brackets_res), line=line_num)
                elif missing_curly_brackets_res > 0:
                    self.add_message(error, "missing_brackets.curly.closing",
                                     count=abs(missing_curly_brackets_res), line=line_num)

    def run_indent_check(self, path: str) -> NoReturn:
        """
        # TODO needs a lot of work
        Run a check to see if the given file contains any indentation errors
        and add simple message according to the response of the check.
        :param path: Path to file.
        """
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

    #######
    #
    # Helper functions
    #
    #######

    def add_message(self, error: Any, code: str, **namespace) -> NoReturn:
        """
        Add an error message to the list of found messages
        :param error: Object representing the found error for example Parso PythonErrorNode or IndentationErrorType
        :param code: Code representing the type of error in messages.py
        :param namespace: context specific parameters to add to the error message,
         must be defined in the message found in messages.py
        """
        self.messages.append((error, get_formatted_message(code, **namespace)))

    def is_not_def_error(self) -> bool:
        """
        Check if any function definition error has been found
        :return: True/False
        """
        return self.invalid_function_def_res is None or not self.invalid_function_def_res
