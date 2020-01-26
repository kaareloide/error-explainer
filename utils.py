def read_file(path):
    with open(path, "r") as input_file:
        return input_file.read()


def is_syntax_error(issue):
    return "SyntaxError" in issue.message
