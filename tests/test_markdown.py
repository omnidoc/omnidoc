from commonmark import Parser
from omnidoc.markdown import markdown_to_tree, _md_ast_children
from omnidoc.markdown import tree_to_sphinx_node
from omnidoc.markdown import MarkdownTransformer
from lark import Lark

example_md = """
# Heading1
That is paragraph text.
## Heading2
This is a paragraph2.
*Italic*
**Bold**

[Link](http://a.com)
![Image](http://url/a.png)
> Blockquote
* List
* List
* List
1. One
2. Two
3. Three

`Inline code` with backticks
```
# code block
print '3 backticks or'
```
"""

parser = Parser()
example_md_ast = parser.parse(example_md)

def test_md_ast_get_children():
    children = _md_ast_children(example_md_ast)
    print([x.t for x in children])
    assert [x.t for x in children] == ['heading', 'paragraph', 'heading', 'paragraph', 'paragraph', 'block_quote', 'list', 'list', 'paragraph', 'code_block']


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
    test_md_ast_get_children()
    test_markdown_to_tree()
    test_tree_to_sphinx_node()