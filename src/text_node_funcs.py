from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        list_of_text = node.text.split(delimiter)
        for i in range(len(list_of_text)):
            if i % 2 == 0 and list_of_text[i] != "":
                new_nodes.append(TextNode(list_of_text[i], node.text_type, node.url))
            elif i % 2 == 1 and list_of_text[i] != "":
                new_nodes.append(TextNode(list_of_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        split_text = re.split(r"!\[.*?\]\(.*?\)", node.text)
        extracted_images = extract_markdown_images(node.text)
        for i in range(len(split_text)):
            if split_text[i] != "":
                new_nodes.append(TextNode(split_text[i], node.text_type, node.url))
            if i < len(split_text) - 1:
                new_nodes.append(TextNode(extracted_images[i][0], TextType.IMAGE, extracted_images[i][1]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        split_text = re.split(r"(?<!!)\[.*?\]\(.*?\)", node.text)
        extracted_links = extract_markdown_links(node.text)
        for i in range(len(split_text)):
            if split_text[i] != "":
                new_nodes.append(TextNode(split_text[i], node.text_type, node.url))
            if i < len(split_text) - 1:
                new_nodes.append(TextNode(extracted_links[i][0], TextType.LINK, extracted_links[i][1]))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes