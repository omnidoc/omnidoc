from commonmark import Parser
from omnidoc.markdown import markdown_to_tree, _md_ast_children

example_md = """
# Heading 1

That is paragraph text.


## Subsection

Also awesome *text*
"""
parser = Parser()
example_md_ast = parser.parse(example_md)


def test_md_ast_get_children():
    children = _md_ast_children(example_md_ast)
    assert [x.t for x in children] == [
        'heading', 'paragraph', 'heading', 'paragraph'
    ]


def test_markdown_to_tree():
    tree = markdown_to_tree(example_md_ast)
    print(tree.pretty())
    # TODO: write test


if __name__ == "__main__":
    test_markdown_to_tree()
