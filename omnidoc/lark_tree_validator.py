"""Tree validator based on Lark grammar

TODO: Move to lark-parser
"""

from lark import UnexpectedToken

from .lark_tree_matcher import TreeMatcher


class TreeValidator:
    "Validate a tree based on Lark grammar"

    def __init__(self, lark_inst):
        self.ltm = TreeMatcher(lark_inst)

    def _validate_tree(self, tree, rulename=None):
        "rulename used for disambiguating templates"
        res = self.ltm.match_tree(tree, rulename)
        assert len(res.children) == len(res.meta.orig_expansion)
        for child, symbol in zip(res.children, res.meta.orig_expansion):
            self._validate_tree(child, symbol.name)
        return res

    def validate_tree(self, tree):
        try:
            self._validate_tree(tree)
            return True
        except UnexpectedToken:
            return False
