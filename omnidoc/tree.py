import lark

from .typesystem import TreeType


class Tree(lark.Tree):
    def __init__(self, data, children, source_obj=None, meta=None):
        super().__init__(data, children, meta)
        self.source_obj = source_obj

    def deduce_type(self):
        return TreeType(type(self), {t.data for t in self.iter_subtrees()})
