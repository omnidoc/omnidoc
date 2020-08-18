from commonmark import Parser
from omnidoc.markdown import markdown_to_tree

example_md = """
# Heading 1

That is paragraph text.


## Subsection

Also awesome *text*
"""


def test_markdown_to_tree():
    parser = Parser()
    ast = parser.parse(example_md)
    markdown_to_tree(ast)


if __name__ == "__main__":
    test_markdown_to_tree()
