import commonmark
import docutils.core

from omnidoc.markdown import _md_ast_children, markdown_to_tree, \
    docutils_to_tree, tree_to_docutils

example_md = """
# Heading 1

That is paragraph text.


## Subsection

Also awesome *text*
"""
example_md_ast = commonmark.Parser().parse(example_md)

example_rst = """
Heading 1
=========

That is paragraph text.

Subsection
----------

Also awesome *text*
"""
example_docutils_ast = docutils.core.publish_doctree(example_rst)


def test_md_ast_get_children():
    children = _md_ast_children(example_md_ast)
    assert [x.t for x in children] == [
        'heading', 'paragraph', 'heading', 'paragraph'
    ]


def test_markdown_to_tree():
    tree = markdown_to_tree(example_md_ast)
    print(tree.pretty())
    # TODO: write test


def test_docutils_to_tree():
    tree = docutils_to_tree(example_docutils_ast)
    print(tree.pretty())
    # TODO: write test


def test_tree_to_docutils():
    tree = docutils_to_tree(example_docutils_ast)
    docutils_tree = tree_to_docutils(tree)
    print('source:', example_docutils_ast.pformat())
    print('output:', docutils_tree.pformat())
    # TODO: write test

if __name__ == "__main__":
    test_tree_to_docutils()
