from htmlnode import LeafNode
from textnode import TextNode, TextType

import re

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url:
                return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url and text_node.text:
                return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text node type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    all_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            splitted = node.text.replace("\n", " ").split(delimiter)
            for i in range(0, len(splitted)):
                if i % 2 == 0:
                    all_nodes.append(TextNode(splitted[i], TextType.TEXT))
                else:
                    all_nodes.append(TextNode(splitted[i], text_type))
        else:
            all_nodes.append(node)
    return list(filter(lambda x: not x.text == "", all_nodes))

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)

def extract_markdown_links(text:str) -> list[tuple[str, str]]:
    return re.findall(r"(?:^|[^!])\[([^\]]*)\]\(([^\)]*)\)", text)

def split_node_images(old_nodes: list[TextNode]) -> list[TextNode]:
    all_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_to_split = node.text
            matches = extract_markdown_images(node.text)
            if len(matches):
                for match in matches:
                    separator = f'![{match[0]}]({match[1]})'
                    splitted = text_to_split.split(separator)
                    all_nodes.extend([TextNode(splitted[0], TextType.TEXT), TextNode(match[0], TextType.IMAGE, url=match[1])])
                    text_to_split = splitted[1]
                all_nodes.append(TextNode(text_to_split, TextType.TEXT))
            else:
                all_nodes.append(node)
        else:
            all_nodes.append(node)
    return list(filter(
        lambda x:not (x.text == "" and x.text_type == TextType.TEXT),
        all_nodes))

def split_node_links(old_nodes: list[TextNode]) -> list[TextNode]:
    all_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_to_split = node.text
            matches = extract_markdown_links(node.text)
            if len(matches):
                for match in matches:
                    splitted = text_to_split.split(f'[{match[0]}]({match[1]})')
                    all_nodes.extend([TextNode(splitted[0], TextType.TEXT), TextNode(match[0], TextType.LINK, url=match[1])])
                    text_to_split = splitted[1]
                all_nodes.append(TextNode(text_to_split, TextType.TEXT))
            else:
                all_nodes.append(node)
        else:
            all_nodes.append(node)

    return list(filter(lambda x: not (x.text == "" and x.text_type == TextType.TEXT),
                       all_nodes))

def text_to_textnode(text: str) -> list[TextNode]:
    initial_node = TextNode(text, TextType.TEXT)
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_node_links(split_node_images([initial_node])),
                "_",
                TextType.ITALIC
            ),
            "`",
            TextType.CODE
        ),
        "**",
        TextType.BOLD
    )
