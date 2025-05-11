import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text Node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node with url", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")

    def test_compare_url(self):
        node = TextNode("This is a text node with url", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node with no url", TextType.TEXT)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
