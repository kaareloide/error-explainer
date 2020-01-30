import parso
import os
from utils import *
from simple_message_creator import get_simple_error_messages
from search_utils import *

if __name__ == "__main__":
    sample_path = "firendly_traceback_tests/raise_indentation_error3.py"
    #sample_path = "samples/invalid_def.py"
    filename = os.path.abspath(sample_path)
    grammar = parso.load_grammar()
    #print(get_lines(filename, [2]))
    module = grammar.parse(read_file(filename))
    errors = grammar.iter_errors(module)
    # print(is_syntax_error(errors[0]))
    #print(get_defined_names(module.get_root_node()))
    if len(errors) > 0:
        # Errors found
        found_errors = find_nodes_of_type(module.get_root_node(), parso.python.tree.PythonErrorNode)
        print(found_errors)
        #print(found_errors[0].get_code())
        print(get_simple_error_messages(module.get_root_node(), filename))
