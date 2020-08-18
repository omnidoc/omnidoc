import lark

from .typesystem import TreeType


class Tree(lark.Tree):
    def deduce_type(self):
        return TreeType(type(self), {t.data for t in self.iter_subtrees()})
