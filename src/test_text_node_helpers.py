import unittest
from textnode import TextNode, TextType
from text_node_helpers import extract_markdown_images, extract_markdown_links, split_node_images, split_node_links, split_nodes_delimiter, text_node_to_html_node, text_to_textnode

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_props(self):
        html_node1 = text_node_to_html_node(TextNode("anchor text", TextType.LINK, url="https://www.boot.dev"))
        html_node2 = text_node_to_html_node(TextNode("alternative text", TextType.IMAGE, url="https://www.boot.dev"))
        self.assertListEqual([html_node1.value, html_node1.props], ["anchor text", {"href": "https://www.boot.dev"}])
        self.assertListEqual([html_node2.value, html_node2.props], ["", {"src": "https://www.boot.dev", "alt": "alternative text"}])

    def test_failure(self):
        text_node = TextNode("this is some text", "random")
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(text_node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delimiters(self):
        code_node = TextNode("This is text with `code block` word", TextType.TEXT)
        italic_node = TextNode("This is text with _italic block_ word", TextType.TEXT)
        bold_node = TextNode("This is text with **bold block** word", TextType.TEXT)
        splitted_code = split_nodes_delimiter([code_node], "`", TextType.CODE)
        splitted_italic = split_nodes_delimiter([italic_node], "_", TextType.ITALIC)
        splitted_bold = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertListEqual([splitted_code, splitted_italic, splitted_bold], [
            [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ],
            [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
            ],
            [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
            ]
        ])

    def test_multiple_nodes(self):
        input_nodes = [
            TextNode("First node with `code block` inside", TextType.TEXT),
            TextNode("Second node with `code block` inside", TextType.TEXT),
            TextNode("Third node with `code block` inside", TextType.TEXT)
        ]
        splitted = split_nodes_delimiter(input_nodes, "`", TextType.CODE)
        self.assertEqual(splitted, [
            TextNode("First node with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
            TextNode("Second node with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
            TextNode("Third node with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ])

    def test_starting_ending_delimiter(self):
        input_nodes = [
            TextNode("`code block` at the start", TextType.TEXT),
            TextNode("block is at the end `code block`", TextType.TEXT),
            TextNode("`only code block`", TextType.TEXT),
        ]
        splitted = split_nodes_delimiter(input_nodes, "`", TextType.CODE)
        self.assertEqual(splitted,
                         [
                             TextNode("code block", TextType.CODE),
                             TextNode(" at the start", TextType.TEXT),
                             TextNode("block is at the end ", TextType.TEXT),
                             TextNode("code block", TextType.CODE),
                             TextNode("only code block", TextType.CODE),
                         ])

class TestImageAndLinkExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_textract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual(matches, [("link", "https://www.boot.dev")])

    def test_multiple_results_and_beginning(self):
        link_matches = extract_markdown_links(
            "[these are](https://www.boot.dev) multiple [links](https://www.kuroashi.dev)"
        )
        image_matches = extract_markdown_images(
            "![these are](https://someimage.jpeg) multiple ![images](https://somemoreimage.png)"
        )
        self.assertListEqual(
            [link_matches, image_matches],
            [
                [("these are", "https://www.boot.dev"), ("links", "https://www.kuroashi.dev")],
                [("these are", "https://someimage.jpeg"), ("images", "https://somemoreimage.png")]
            ]
        )

    def test_link_and_image_simultaneously(self):
        string = "This string has a [link](https://www.boot.dev) and an ![image](https://someimage.jpeg)"
        link_match = extract_markdown_links(string)
        image_match = extract_markdown_images(string)
        self.assertListEqual([link_match, image_match], [
            [("link", "https://www.boot.dev")],
            [("image", "https://someimage.jpeg")]
        ])

class TestImageAndLinkSplitter(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_node_images([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [one](https://www.kuroashi.dev)",
            TextType.TEXT,
        )
        new_nodes = split_node_links([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://www.kuroashi.dev"),
            ]
        )

    def test_split_image_multiple_nodes_and_position(self):
        old_nodes = [
            TextNode(
                "This is a node with just one ![image](https://someimage.jpeg)",
                TextType.TEXT
            ),
            TextNode(
                "![This](https://anotherimage.png) has the image at the start",
                TextType.TEXT
            ),
        ]
        new_nodes = split_node_images(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a node with just one ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://someimage.jpeg"),
                TextNode("This", TextType.IMAGE, "https://anotherimage.png"),
                TextNode(" has the image at the start", TextType.TEXT),
            ]
        )
    def test_split_link_multiple_nodes_and_position(self):
        old_nodes = [
            TextNode(
                "This is text with just one [link](https://www.boot.dev)",
                TextType.TEXT
            ),
            TextNode(
                "[This](https://www.kuroashi.dev) has the link at the start",
                TextType.TEXT
            )
        ]
        new_nodes = split_node_links(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with just one ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("This", TextType.LINK, "https://www.kuroashi.dev"),
                TextNode(" has the link at the start", TextType.TEXT),
            ]
        )

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_text_node(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnode(text)
        self.assertListEqual(
            nodes,
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        )

    def test_starting_nodes(self):
        text_start = "**This string** starts with some _bolded_ text."
        text_end = "This string has a _code inline block_ `at the end`"
        nodes_start = text_to_textnode(text_start)
        nodes_end = text_to_textnode(text_end)
        self.assertListEqual([
            nodes_start,
            nodes_end
        ], [
            [
                TextNode("This string", TextType.BOLD),
                TextNode(" starts with some ", TextType.TEXT),
                TextNode("bolded", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
            [
                TextNode("This string has a ", TextType.TEXT),
                TextNode("code inline block", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("at the end", TextType.CODE),
            ]
        ])

    def test_empty(self):
        nodes = text_to_textnode("")
        self.assertEqual(nodes, [])
