from commonmark import Parser
from omnidoc.markdown import markdown_to_tree, _md_ast_children
from omnidoc.markdown import tree_to_sphinx_node
from omnidoc.markdown import MarkdownTransformer
from lark import Lark

example_md = """
# Heading1
That is paragraph text.
# Heading2
This is a paragraph2.
"""


parser = Parser()
example_md_ast = parser.parse(example_md)
# print(md_parser.parse(example_md).pretty())

def test_md_ast_get_children():
    children = _md_ast_children(example_md_ast)
    assert [x.t for x in children] == [
        'heading', 'paragraph', 'heading', 'paragraph'
    ]


def test_markdown_to_tree():
    tree = markdown_to_tree(example_md_ast)
    print(tree.pretty())
    # TODO: write test

def test_tree_to_sphinx_node():
	tree = markdown_to_tree(example_md_ast)
	larkTree=MarkdownTransformer().transform(tree)
	node = tree_to_sphinx_node(larkTree)
	print(node)	

if __name__ == "__main__":
    # test_md_ast_get_children()
    # test_markdown_to_tree()
    test_tree_to_sphinx_node()