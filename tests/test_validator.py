from copy import deepcopy

from lark import Lark

from omnidoc.tree_validator import validate_tree

p = Lark("""
start: heading paragraph{text} heading paragraph{_p1} _p1

_p1: text emph

heading: text?
paragraph{elem}: elem
emph: text

text:
""")  # , ambiguity='explicit')


def _swap_children(t, a, b):
    t.children[a], t.children[b] = t.children[b], t.children[a]


def test_validate_templates():
    good_tree = p.parse('')
    assert validate_tree(p, good_tree)

    # Swap 1 and 3, which are same template with different args
    bad_tree = deepcopy(good_tree)
    _swap_children(bad_tree, 1, 3)
    assert not validate_tree(p, bad_tree)
