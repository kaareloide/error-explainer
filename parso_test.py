import parso


def read_file(path):
    with open(path, "r") as input_file:
        return input_file.read()


def is_syntax_error(issue):
    return "SyntaxError" in issue.message


def get_line_location(error_node):
    return error_node.get_start_pos_of_prefix()[0]


def find_error_nodes(root_node):
    nodes = []
    stack = [root_node]
    while stack:
        cur_node = stack[0]
        stack = stack[1:]
        if type(cur_node) == parso.python.tree.PythonErrorNode:
            nodes.append(cur_node)
        try:
            for child in cur_node.children:
                stack.append(child)
        except AttributeError:
            pass
    return nodes


def check_missing_parens(error_node):
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
    #todo return what statement was used
    colon_statements = [
        "if",
        "else",
        "elif",
        "try",
        "exept",
        "while",
        "for",
        "def",
        "class"
    ]
    error_code = error_node.get_code()
    error_code = error_code.strip()

    if any(statement in error_code for statement in colon_statements):
        return ":" not in error_code
    return False


def get_simple_error_messages(root_node):
    messages = []
    found_errors = find_error_nodes(root_node)
    for error in found_errors:
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
        elif check_missing_colon(error):
            #todo get statement type from method and use in message
            messages.append((error, f"Missing colon before an indentation block on line {line_num}."
                                    f""))

    return messages


if __name__ == "__main__":
    sample_path = "samples/missing_colon.py"
    grammar = parso.load_grammar()
    module = grammar.parse(read_file(sample_path))
    errors = grammar.iter_errors(module)
    # print(is_syntax_error(errors[0]))
    if len(errors) > 0:
        # Errors found
        print(find_error_nodes(module.get_root_node())[0])
        found_error = find_error_nodes(module.get_root_node())[0]
        print(get_simple_error_messages(module.get_root_node()))
