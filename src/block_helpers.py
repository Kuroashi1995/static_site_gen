import re
from block_type import BlockType

def markdown_to_blocks(md: str) -> list[str]:
    splitted = md.split("\n\n")
    blocks = []
    for split in splitted:
        blocks.append(split.strip())
    return list(filter(lambda block: not block == "", blocks))

def block_to_block_type(block: str) -> BlockType:
    #Function to check lines starting characters
    def check_lines_start(lines:list[str], pattern: str):
        if len(lines) == 1:
            return lines[0].startswith(pattern)
        else:
            return check_lines_start(lines[1:], pattern) and lines[0].startswith(pattern)

    #Function to check increasing ordered startign characters
    def check_ordered_list(lines: list[str], checker: int):
        if len(lines) == 1:
            return lines[0].startswith(f"{checker}. ")
        else:
            return lines[0].startswith(f"{checker}. ") and check_ordered_list(lines[1:], checker + 1)

    heading_pattern = re.compile(r"^#{1,6} ")
    lines = block.split("\n")
    if heading_pattern.search(block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif check_lines_start(lines, ">"):
        return BlockType.QUOTE
    elif check_lines_start(lines, "- "):
        return BlockType.UNORDERED_LIST
    elif check_ordered_list(lines, 1):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
