from omnidoc import TreeType, Tree


class UnknownTree:
    pass


def test_simple_type_system():
    t1 = TreeType(Tree, frozenset({'a', 'b', 'c'}))
    assert not (t1 <= UnknownTree())

    t2 = TreeType(Tree, frozenset({'a', 'b', 'c', 'd'}))
    assert t1 <= t2
    assert not (t2 <= t1)

    t3 = Tree('a', [Tree('b', [3])]).deduce_type()
    assert t3 <= t1
    assert t3 <= t2


if __name__ == '__main__':
    test_simple_type_system()