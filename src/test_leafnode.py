import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf_node = LeafNode("p", "this is a paragraph")
        self.assertEqual(leaf_node.to_html(), "<p>this is a paragraph</p>")
        leaf_node2 = LeafNode("p", None)
        with self.assertRaises(ValueError):
            html = leaf_node2.to_html()

    def test_instantiation(self):
        with self.assertRaises(TypeError):
            leaf_node = LeafNode(props= None)
