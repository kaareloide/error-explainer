import parso
from checks import *
from search_utils import *
import utils
from message_provider import MessageProvider


class SimpleMessageCreator(object):

    def __init__(self):
        self.message_provider = MessageProvider()
        self.message_provider.parse_messages()
        self.messages = []
        self.missing_brackets_res = None
        self.invalid_function_def_res = None

    def add_message(self, error, code, **namespace):
        self.messages.append((error, self.message_provider.get_formatted_message(code, **namespace)))

    def run_check_invalid_function_def(self, error, path, line_num):
        # for some reason parso returns wrong line number in this case
        line_num += 1

        self.invalid_function_def_res = check_invalid_function_def(error)
        if self.invalid_function_def_res:
            error_line = utils.get_lines(path, [line_num-1])[0]
            print(error_line)
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


    def run_missing_brackets_checks(self, error, path, line_num):
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

    def get_simple_error_messages(self, root_node, path):
        """
        searches for all error nodes and then runs error checks on the found nodes
        :param root_node: root node of the partial AST given by parso
        :param path path to the python file
        :return: list of tuples in the form of (error node, simple message) of all the found errors
        """
        found_errors = find_nodes_of_type(root_node, parso.python.tree.PythonErrorNode)
        for error in found_errors:
            line_num = get_line_location(error)
            missing_colon_result = None
            self.run_check_invalid_function_def(error, path, line_num)

            self.run_missing_brackets_checks(error, path, line_num)

            if sum(self.missing_brackets_res) == 0 and self.is_not_def_error():
                missing_colon_result = check_missing_colon(error)

            if check_print_missing_brackets(error):
                self.add_message(error, "missing_brackets.print", line=line_num)
            elif missing_colon_result is not None:
                self.add_message(error, "missing_colon", line=line_num, statement=missing_colon_result)

        return self.messages

    def is_not_def_error(self):
        return self.invalid_function_def_res is None or not self.invalid_function_def_res
