import parso
import os

colon_statements = {
        "if": parso.python.tree.IfStmt,
        "try": parso.python.tree.TryStmt,
        "while": parso.python.tree.WhileStmt,
        "for": parso.python.tree.ForStmt,
        "def": parso.python.tree.Function,
        "class": parso.python.tree.Class,
        "with": parso.python.tree.WithStmt
    }


def read_file(path):
    with open(path, "r") as input_file:
        return input_file.read()


def is_syntax_error(issue):
    return "SyntaxError" in issue.message


def get_line_location(error_node):
    return error_node.get_start_pos_of_prefix()[0]


def find_nodes_of_type(root_node, node_type):
    nodes = []
    stack = [root_node]
    while stack:
        cur_node = stack[0]
        stack = stack[1:]
        if type(cur_node) == node_type:
            nodes.append(cur_node)
        try:
            for child in cur_node.children:
                stack.append(child)
        except AttributeError:
            pass
    return nodes


def check_missing_parens(error_node):
    #todo doesn't seem to work with opening parens
    parens = 0
    error_code = error_node.get_code()
    error_code = error_code.strip()
    stack = list(error_code)

    while stack:
        current = stack.pop(0)
        if current == "(":
            parens += 1
        elif current == ")":
            parens -= 1
    return parens


def check_print_missing_parens(error_node):
    error_code = error_node.get_code()
    error_code = error_code.strip()
    if error_code == "print":
        return True
    return False


def check_missing_colon(error_node):
    error_code = error_node.get_code()
    error_code = error_code.strip()

    for statement in colon_statements:
        if statement in error_code and ":" not in error_code:
            return statement
    return None


def get_simple_error_messages(root_node):
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


def find_defined_vars(root_node):
    var_names = []
    exprs = find_nodes_of_type(root_node, parso.python.tree.ExprStmt)
    for expr in exprs:
        var_names.append(expr.get_defined_names())
    return var_names


def find_defined_functions(root_node):
    function_names = []
    functions = find_nodes_of_type(root_node, parso.python.tree.Function)
    for func in functions:
        function_names.append(func.name)
    return function_names


def get_defined_names(root_node):
    defined_names = []
    defined_names.extend(find_defined_functions(root_node))
    defined_names.extend(find_defined_vars(root_node))
    return defined_names


if __name__ == "__main__":
    sample_path = "samples/defs.py"
    filename = os.path.abspath(sample_path)
    grammar = parso.load_grammar()
    module = grammar.parse(read_file(filename))
    errors = grammar.iter_errors(module)
    # print(is_syntax_error(errors[0]))
    print(get_defined_names(module.get_root_node()))
    if len(errors) > 0:
        # Errors found
        found_error = find_nodes_of_type(module.get_root_node(), parso.python.tree.PythonErrorNode)[0]
        print(get_simple_error_messages(module.get_root_node()))
