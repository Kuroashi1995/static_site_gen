import unittest

from block_helpers import block_to_block_type, markdown_to_blocks
from block_type import BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_lines(self):
        md = """
This is just to test some empty lines




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just to test some empty lines"])

    def test_completely_empty(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

class TestBlockToBlockType(unittest.TestCase):
    # Paragraphs tests
    def test_paragraphs(self):
        md = """
These are going to be all simple paragraphs

To test how the function works, the first block is a single line
this one has multiple ones

"""
        blocks = markdown_to_blocks(md)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH
            ]
        )

    # Heading tests
    def test_headings(self):
        md = """
# This is heading 1

## This is heading 2

### This is heading 3

#### This is heading 4

##### This is heading 5

###### This is heading 6

####### This is no heading

This either

#this neither
"""
        blocks = markdown_to_blocks(md)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))

        self.assertListEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )

    # Code block test
    def test_code_blocks(self):
        md = """
```This is going to test code blocks```

```The first one had only one line
This one on the other hand doesnt```

```
This one also has mutliple
lines of code
as my codebase
```

```This one shouldn't be a code block

This one either```
"""
        blocks = markdown_to_blocks(md)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            block_types,
            [
                BlockType.CODE,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )

    #Quote block tests
    def test_quote_blocks(self):
        md = """
>This is going to test quote blocks

>The first one
>And this one too should
>be quote blocks

>This is
not a 
>quote block

This one
>isn't one
>as well
"""
        blocks = markdown_to_blocks(md)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            block_types,
            [
                BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )

    #Unordered lists test
    def test_unordered_lists(self):
        md = """
- This is going
- To test
- Some unordered lists

- This is also an unordered list

- This
is not
- a list

-This
-either
"""
        blocks = markdown_to_blocks(md)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            block_types,
            [
                BlockType.UNORDERED_LIST,
                BlockType.UNORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )

    # Ordered lists tests
    def test_ordered_lists(self):
        md = """
1. This is going
2. To test ordered
3. Lists

1. This is also an ordered list

3. This is
1. Not one
2. At all

1.This one
2.Isn't one
3.Either
"""
        blocks = markdown_to_blocks(md)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            block_types,
            [
                BlockType.ORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )
