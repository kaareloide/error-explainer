"""
Map of statements tha are followed by a colon and their parso node counterparts
"""
import parso


colon_statements = {
    "if": parso.python.tree.IfStmt,
    "try": parso.python.tree.TryStmt,
    "while": parso.python.tree.WhileStmt,
    "for": parso.python.tree.ForStmt,
    "def": parso.python.tree.Function,
    "class": parso.python.tree.Class,
    "with": parso.python.tree.WithStmt,
    "else": parso.python.tree.IfStmt,
    "elif": parso.python.tree.IfStmt,
}
