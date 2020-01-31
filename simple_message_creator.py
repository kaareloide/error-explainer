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

    def add_message(self, error, code, **namespace):
        self.messages.append((error, self.message_provider.get_formatted_message(code, **namespace)))

    def get_simple_error_messages(self, root_node, path):
        """
        searches for all error nodes and then runs error checks on the found nodes
        :param root_node: root node of the partial AST given by parso
        :param path path to the python file
        :return: list of tuples in the form of (error node, simple message) of all the found errors
        """
        found_errors = find_nodes_of_type(root_node, parso.python.tree.PythonErrorNode)
        for error in found_errors:
            missing_colon_result = None
            line_num = get_line_location(error)
            if check_invalid_function_def(error):
                invalid_function_name_res = check_invalid_function_name(utils.get_lines(path,
                                                                                        [get_line_location(error)])[0])
                print(invalid_function_name_res)
                if invalid_function_name_res is not None:
                    self.add_message(error, "invalid_function_name",
                                     line=line_num, invalid_name=invalid_function_name_res)

            # All error checks go here
            missing_brackets_res = check_missing_brackets(error)
            missing_normal_brackets_res = missing_brackets_res[0]
            missing_square_brackets_res = missing_brackets_res[1]
            missing_curly_brackets_res = missing_brackets_res[2]

            if sum(missing_brackets_res) != 0:
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
            else:
                missing_colon_result = check_missing_colon(error)

            if check_print_missing_brackets(error):
                self.add_message(error, "missing_brackets.print", line=line_num)
            elif missing_colon_result is not None:
                self.add_message(error, "missing_colon", line=line_num, statement=missing_colon_result)

        return self.messages
