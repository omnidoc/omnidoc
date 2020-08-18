from .lark_tree_validator import TreeValidator

def validate_tree(p, t):
    return TreeValidator(p).validate_tree(t)
