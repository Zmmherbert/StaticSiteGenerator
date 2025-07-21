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

    def test_block_to_block_type(self):
        block_type_heading = block_to_block_type('### This is a heading')
        self.assertEqual(block_type_heading, BlockType.HEADING)
        block_type_code = block_to_block_type('```THERES SOME CODE HERE ```')
        self.assertEqual(block_type_code, BlockType.CODE)
        block_type_quote = block_to_block_type('>QUOTE 1\n> QUOTE 2')
        self.assertEqual(block_type_quote, BlockType.QUOTE)
        block_type_unordered_list = block_to_block_type('- item\n- another item\n- and another')
        self.assertEqual(block_type_unordered_list, BlockType.UNORDERED_LIST)
        block_type_ordered_list = block_to_block_type('1. item 1\n2. item 2\n3. item 3')
        self.assertEqual(block_type_ordered_list, BlockType.ORDERED_LIST)
        block_type_paragraph = block_to_block_type('Just some words and shit\nidk really')
        self.assertEqual(block_type_paragraph, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()