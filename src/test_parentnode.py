import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_creation(self):
        with self.assertRaises(TypeError):
            parent_node = ParentNode(props={"some": "value"})

    def test_to_html_fail(self):
        parent_node1 = ParentNode(None, [LeafNode("p", "some value")])
        parent_node2 = ParentNode("p", None)
        with self.assertRaises(ValueError):
            html1 = parent_node1.to_html()
        with self.assertRaises(ValueError):
            html2 = parent_node2.to_html()

    def test_multiple_children(self):
        children_nodes = [LeafNode("p", "this is a little paragraph"), LeafNode("div", "a little div")]
        parent_node =  ParentNode("pre", children_nodes, props={"class-name": "someclassname"})
        self.assertEqual(parent_node.to_html(), '<pre class-name="someclassname" ><p>this is a little paragraph</p><div>a little div</div></pre>')
