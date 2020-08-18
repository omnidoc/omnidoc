import lark
from .tree import Tree


def _md_ast_children(markdown_ast):
    x = markdown_ast.first_child
    children = []
    while x:
        children.append(x)
        x = x.nxt

    return children


def markdown_to_tree(markdown_ast):
    """Convert markdown AST to Tree

    Args:
        markdown_ast (commonmark.node.Node): Parsed markdown AST. Usually
            generated by commonmark.Parser().parse(text).

    Returns:
        Tree: Tree representation of markdown's AST.
    """
    return Tree(
        data=markdown_ast.t,
        children=[markdown_to_tree(child)
                  for child in _md_ast_children(markdown_ast)],
        source_obj=markdown_ast
    )


def docutils_to_tree(docutils_ast):
    """Convert docutils AST to Tree

    Args:
        docutils_ast (docutils.nodes.Node): Docutils node to be converted to
            Tree.

    Returns:
        Tree: Tree representation of docutils tree.
    """
    return Tree(
        data=docutils_ast.tagname,
        children=[docutils_to_tree(x) for x in docutils_ast.children],
        source_obj=docutils_ast
    )


class MarkdownTransformer(lark.Transformer):
    """Convert MarkdownTree to SphinxNodeTree."""
    pass


def tree_to_sphinx_node(tree):
    """Convert tree representation to sphinx node API.

    Args:
        tree (lark.Tree): Tree represntation to sphinx node API.
    """
    raise NotImplementedError