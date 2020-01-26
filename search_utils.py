import parso


def find_nodes_of_type(root_node, node_type):
    """
    :param root_node: root node of the partial AST given by parso
    :param node_type: type of node to search for
    :return: nodes of type node_type found
    """
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


def find_defined_vars(root_node):
    """
    find all the defined variables
    :param root_node: root node of the partial AST given by parso
    :return: list of found variable names
    """
    var_names = []
    exprs = find_nodes_of_type(root_node, parso.python.tree.ExprStmt)
    for expr in exprs:
        var_names.append(expr.get_defined_names())
    return var_names


def find_defined_functions(root_node):
    """
    find all defined functions
    :param root_node: root node of the partial AST given by parso
    :return: list of found function names
    """
    function_names = []
    functions = find_nodes_of_type(root_node, parso.python.tree.Function)
    for func in functions:
        function_names.append(func.name)
    return function_names


def get_defined_names(root_node):
    """
    find all defined names of functions and variables
    :param root_node: root_node: root node of the partial AST given by parso
    :return: list of found function and variable names
    """
    defined_names = []
    defined_names.extend(find_defined_functions(root_node))
    defined_names.extend(find_defined_vars(root_node))
    return defined_names


def get_line_location(error_node):
    """
    :param error_node: node with an error
    :return: index of the starting position on the error line
    """
    return error_node.get_start_pos_of_prefix()[0]
