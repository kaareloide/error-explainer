from typing import List

import parso


def find_nodes_of_type(
    root_node: parso.python.tree.Module, node_type: parso.python.tree.PythonBaseNode
) -> List[parso.python.tree.PythonBaseNode]:
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


def find_defined_vars(root_node: parso.python.tree.Module) -> List[str]:
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


def find_defined_functions(root_node: parso.python.tree.Module) -> List[str]:
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


def get_defined_names(root_node: parso.python.tree.Module) -> List[str]:
    """
    find all defined names of functions and variables
    :param root_node: root_node: root node of the partial AST given by parso
    :return: list of found function and variable names
    """
    defined_names = []
    defined_names.extend(find_defined_functions(root_node))
    defined_names.extend(find_defined_vars(root_node))
    return defined_names


def get_line_location_end(error_node: parso.python.tree.Module) -> int:
    """
    :param error_node: node
    :return: line number of the end of the error
    """
    return error_node.end_pos[0]


def get_line_location_start(error_node: parso.python.tree.Module) -> int:
    """
    :param error_node: node
    :return: line number of the start of the error error
    """
    return error_node.get_start_pos_of_prefix()[0]


def get_location_on_line(error_node: parso.python.tree.Module) -> int:
    """
    :param error_node: node
    :return: what position is the error at on the line
    """
    return error_node.get_start_pos_of_prefix()[1]
