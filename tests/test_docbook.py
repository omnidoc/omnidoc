from lxml.etree import QName
from lxml import etree
from omnidoc.docbook import xmlTree_to_LarkTree, docbookTranformer, tree_to_sphinx_node

root = etree.parse('part01.xml').getroot()

def test_xmlTree_to_LarkTree():
    tree = xmlTree_to_LarkTree(root)
    print(tree)
    # TODO: write test

def test_docbookTranformer():
    tree = xmlTree_to_LarkTree(root)
    transformedTree = docbookTranformer().transform(tree)
    print(test_docbookTranformer)
    # TODO: write test

def test_tree_to_sphinx_node():
    tree = xmlTree_to_LarkTree(root)
    transformedTree = docbookTranformer().transform(tree)
    node = tree_to_sphinx_node(transformedTree)
    print(node)
    # TODO: write test

if __name__ == "__main__":
    test_xmlTree_to_LarkTree()
    test_docbookTranformer()
    test_tree_to_sphinx_node()