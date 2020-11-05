import lark

from .typesystem import TreeType


class Tree(lark.Tree):
	def __init__(self, data, children, source_obj=None, meta=None, literal=None, level=None, destination=None, list_data=None):
		super().__init__(data, children, meta)
		self.source_obj = source_obj
		self.literal = literal
		self.level = level
		self.destination = destination
		self.list_data = list_data

	def deduce_type(self):
		return TreeType(type(self), {t.data for t in self.iter_subtrees()})
	


