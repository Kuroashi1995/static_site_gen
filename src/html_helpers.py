from block_helpers import block_to_block_type, markdown_to_blocks
from block_type import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode

import re

from text_node_helpers import text_node_to_html_node, text_to_textnode

def block_type_to_html_tag(block_type: BlockType) -> str:
    match block_type:
        case BlockType.HEADING:
            return "h"
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.CODE:
            return "code"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.QUOTE:
            return "blockquote"
        case _:
            raise ValueError("Block type not recognized")

def text_to_children(text: str, block_type: BlockType) -> list[LeafNode | ParentNode]:
    children = []
    match block_type:
        case BlockType.ORDERED_LIST | BlockType.UNORDERED_LIST:
            pattern = re.compile(r"^\d. |^- ", re.RegexFlag.MULTILINE)
            new_text = pattern.sub("", text)
            lines = new_text.split("\n")
            for line in lines:
                line_children = []
                line_children_text_nodes= text_to_textnode(line)
                for node in line_children_text_nodes:
                    line_children.append(text_node_to_html_node(node))
                children.append(ParentNode("li", line_children))
        case BlockType.CODE:
            pattern = re.compile(r"^```\n|```$", re.RegexFlag.MULTILINE)
            new_text = pattern.sub("", text)
            children.append(LeafNode(None, new_text))
        case BlockType.PARAGRAPH:
            text_nodes = text_to_textnode(text)
            for node in text_nodes:
                children.append(text_node_to_html_node(node))
        case BlockType.QUOTE:
            pattern = re.compile(r"^> ", re.RegexFlag.MULTILINE)
            new_text = pattern.sub("", text)
            text_nodes = text_to_textnode(new_text)
            for node in text_nodes:
                children.append(text_node_to_html_node(node))
        case BlockType.HEADING:
            pattern = re.compile(r"^#{1,6} ")
            new_text = pattern.sub("", text)
            children.append(LeafNode(None, new_text))
        case _:
            raise ValueError("Block type not recognized")
    return children

def markdown_to_html_node(markdown: str) -> HTMLNode:
    # 1. split the text in blocks
    blocks = markdown_to_blocks(markdown)
    nodes = []
    # 2. loop blocks
    for block in blocks:
    #   3. get block type
        block_type = block_to_block_type(block)
    #   4. create html node based on type
    #   5. give it his proper children, code block stays the same
        if block_type == BlockType.CODE:
            nodes.append(ParentNode(
                "pre",
                [ParentNode(
                    block_type_to_html_tag(block_type),
                    text_to_children(block, block_type)
                )]
            ))
        elif block_type == BlockType.HEADING:
            heading_size = len(re.compile(r"^(#{1,6})").findall(block)[0])
            heading_tag = block_type_to_html_tag(block_type) + f"{heading_size}"
            heading_children = text_to_children(block, block_type)
            nodes.append(ParentNode(heading_tag, heading_children))
        else:
            nodes.append(ParentNode(block_type_to_html_tag(block_type), text_to_children(block, block_type)))
    # 6. wrap them up in an Parent Node
    return ParentNode("div", nodes)

def extract_title(markdown: str):
    h1_pattern = re.compile(r"^# (.*)", re.RegexFlag.MULTILINE)
    h1 = h1_pattern.findall(markdown)
    if len(h1) == 0:
        raise Exception("No header found")
    else:
        return h1[0]

