import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_node_funcs import *


class TestConverion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node = TextNode("Hello", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.props, None)

        node = TextNode("Hello", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

        node = TextNode("Hello", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "Hello"})

    def test_delimiter_splitting(self):
        node = TextNode("Hello, go **die** please", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "Hello, go ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "die")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " please")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        old_nodes = [TextNode("Hello, go _die_ please", TextType.TEXT), TextNode("_first_ and _last_", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[1].text, "die")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[3].text, "first")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[5].text, "last")
        self.assertEqual(new_nodes[5].text_type, TextType.ITALIC)

    def test_extraction(self):
        image_matches = extract_markdown_images("[link start](https://) This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)")
        link_matches = extract_markdown_links("[link start](https://) This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
        self.assertListEqual([("link start", "https://"), ("link", "https://www.google.com")], link_matches)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.TEXT), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),], new_nodes)

    def test_split_links(self):
        node = TextNode("This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.TEXT), TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),], new_nodes)

    def test_split_images_and_links(self):
        node = TextNode("[link1](https://) and then ![image](https://) and finally [link2](https://)", TextType.TEXT)
        image_split_nodes = split_nodes_image([node])
        link_split_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("[link1](https://) and then ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://"), TextNode(" and finally [link2](https://)", TextType.TEXT)], image_split_nodes)
        self.assertListEqual([TextNode("link1", TextType.LINK, "https://"), TextNode(" and then ![image](https://) and finally ", TextType.TEXT), TextNode("link2", TextType.LINK, "https://")], link_split_nodes)

    def test_split_multiple_nodes(self):
        old_nodes = [TextNode("[link](url) first node", TextType.TEXT), TextNode(" second node [link](url)", TextType.TEXT), TextNode("![image](url) last node", TextType.TEXT)]
        image_split_nodes = split_nodes_image(old_nodes)
        link_split_nodes = split_nodes_link(old_nodes)
        self.assertListEqual([TextNode("[link](url) first node", TextType.TEXT), TextNode(" second node [link](url)", TextType.TEXT), TextNode("image", TextType.IMAGE, "url"), TextNode(" last node", TextType.TEXT)], image_split_nodes)
        self.assertListEqual([TextNode("link", TextType.LINK, "url"), TextNode(" first node", TextType.TEXT), TextNode(" second node ", TextType.TEXT), TextNode("link", TextType.LINK, "url"), TextNode("![image](url) last node", TextType.TEXT)], link_split_nodes)

    def test_text_to_text_nodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual([TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word and a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" and an ", TextType.TEXT), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev"),], nodes)

if __name__ == "__main__":
    unittest.main()