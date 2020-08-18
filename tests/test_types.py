from unittest import TestCase, main

from omnidoc import TreeType, Tree

class TestTypes(TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        t1 = TreeType(Tree, frozenset({'a', 'b', 'c'}))
        t2 = TreeType(Tree, frozenset({'a', 'b', 'c', 'd'}))
        assert t1 <= t2
        assert not (t2 <= t1)

        t3 = Tree('a', [Tree('b', [3])]).deduce_type()
        assert t3 <= t1
        assert t3 <= t2

if __name__ == '__main__':
    main()