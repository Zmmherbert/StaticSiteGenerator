import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_conversion_funcs import *

class TestBlockFuncs(unittest.TestCase):
    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks("""
Block 1 paragraph





Block 2 paragraph
""")
        self.assertEqual(blocks, ["Block 1 paragraph", "Block 2 paragraph"])

    def test_markdown_to_blocks2(self):
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

if __name__ == "__main__":
    unittest.main()