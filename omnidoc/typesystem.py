from dataclasses import dataclass


class AbstractType:
    pass

@dataclass
class TreeType(AbstractType):
    name: str
    nodeset: frozenset

    def issubtype(self, t):
        assert isinstance(t, TreeType), t

        return self.name == t.name and self.nodeset <= t.nodeset

    def __le__(self, other):
        return self.issubtype(other)