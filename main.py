import parso
import os
from utils import *
from simple_message_creator import get_simple_error_messages

if __name__ == "__main__":
    sample_path = "samples/missing_paren_1.py"
    filename = os.path.abspath(sample_path)
    grammar = parso.load_grammar()
    module = grammar.parse(read_file(filename))
    errors = grammar.iter_errors(module)
    # print(is_syntax_error(errors[0]))
    #print(get_defined_names(module.get_root_node()))
    if len(errors) > 0:
        # Errors found
        # found_error = find_nodes_of_type(module.get_root_node(), parso.python.tree.PythonErrorNode)[0]
        print(get_simple_error_messages(module.get_root_node()))
