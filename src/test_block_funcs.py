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
        
    def test_quoteblock(self):
        md = """
>This is text is a part of a 
>quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>This is text is a part of a quote</blockquote></div>",
    )
        
    def test_headingblock(self):
        md = """
### This is an h3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h3>This is an h3</h3></div>",
    )
        
    def test_ulblock(self):
        md = """
- item 1
- item 2
- item last
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>item 1</li><li>item 2</li><li>item last</li></ul></div>",
    )
        
    def test_olblock(self):
        md = """
1. item 1
2. item 2
3. item last
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>item 1</li><li>item 2</li><li>item last</li></ol></div>",
    )

if __name__ == "__main__":
    unittest.main()