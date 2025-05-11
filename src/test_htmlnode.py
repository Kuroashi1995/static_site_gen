import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        html_node = HTMLNode("div", "value", None, None)
        with self.assertRaises(NotImplementedError):
            html_node.to_html()

    def test_props(self):
        html_node = HTMLNode("img", "link to boot.dev", None, {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(html_node.props_to_html(), ' href="https://www.boot.dev" target="_blank" ')

    def test_empty(self):
        html_node = HTMLNode()
        self.assertListEqual(
            [html_node.tag, html_node.value, html_node.children, html_node.props],
            [None, None, None, None]
        )
