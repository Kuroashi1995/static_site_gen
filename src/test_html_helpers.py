from block_type import BlockType
from html_helpers import block_to_block_type, block_type_to_html_tag, extract_title, text_to_children, markdown_to_html_node

import unittest

from htmlnode import LeafNode

class TestBlockTypeToHTMLTag(unittest.TestCase):
    def test_block_type_to_html_tag(self):
        block_types = [
            BlockType.PARAGRAPH,
            BlockType.CODE,
            BlockType.ORDERED_LIST,
            BlockType.UNORDERED_LIST,
            BlockType.QUOTE
        ]
        tags = []
        for block_type in block_types:
            tags.append(block_type_to_html_tag(block_type))
        self.assertListEqual(
            tags,
            [
                "p",
                "code",
                "ol",
                "ul",
                "q",
            ]
        )

    def test_non_blocktype(self):
        with self.assertRaises(ValueError):
            tag = block_type_to_html_tag("random")

class TestTextToChildren(unittest.TestCase):
    def test_paragraph_children(self):
        text = "This is just a **paragraph** with some _inline_ blocks"
        children = text_to_children(text, BlockType.PARAGRAPH)
        self.assertListEqual(
            children,
            [
                LeafNode(None, "This is just a "),
                LeafNode("b", "paragraph"),
                LeafNode(None, " with some "),
                LeafNode("i", "inline"),
                LeafNode(None, " blocks"),
            ]
        )

    def test_code_children(self):
        text = """```
This is **suposed** to be a _code block_
with a line jump
```"""
        children = text_to_children(text, BlockType.CODE)
        self.assertListEqual(
            children,
            [
                LeafNode(None, "This is **suposed** to be a _code block_\nwith a line jump\n")
            ]
        )

    def test_list_children(self):
        text1 = "- This is\n- An unordered\n- List"
        text2 = "1. This is\n2. An ordered\n3. List"
        chilren1 = text_to_children(text1, BlockType.UNORDERED_LIST)
        chilren2 = text_to_children(text2, BlockType.ORDERED_LIST)
        self.assertListEqual(
            chilren1,
            [
                LeafNode("li", "This is"),
                LeafNode("li", "An unordered"),
                LeafNode("li", "List"),
            ]
        )
        self.assertListEqual(
            chilren2,
            [
                LeafNode("li", "This is"),
                LeafNode("li", "An ordered"),
                LeafNode("li", "List"),
            ]
        )

    def test_quote_children(self):
        text = """>This is suposed
>to **become**
>a _blockquote_"""
        children = text_to_children(text, BlockType.QUOTE)
        self.assertListEqual(
            children,
            [
                LeafNode(None, "This is suposed to "),
                LeafNode("b", "become"),
                LeafNode(None, " a "),
                LeafNode("i", "blockquote"),
            ]
        )

class TestMarkdownToTHML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md1 = """
- This is
- an unordered
- list
"""
        md2 = """
1. This is
2. an ordered
3. list
"""
        node1 = markdown_to_html_node(md1)
        node2 = markdown_to_html_node(md2)
        html1 = node1.to_html()
        html2 = node2.to_html()
        self.assertEqual(
            html1,
            "<div><ul><li>This is</li><li>an unordered</li><li>list</li></ul></div>"
        )
        self.assertEqual(
            html2,
            "<div><ol><li>This is</li><li>an ordered</li><li>list</li></ol></div>"
        )

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# Hello world.")
        self.assertEqual(title, "Hello world.")

    def test_no_title(self):
        with self.assertRaises(Exception):
            title = extract_title("This has no title")

    def test_almost_titles(self):
        md = """
#This is almost a title
## This one is almost a title as well
Not # Quite the title
# Now this is a title
"""
        title = extract_title(md)
        self.assertEqual(title, "Now this is a title")
