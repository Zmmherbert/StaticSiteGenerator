from enum import Enum
import re
from htmlnode import HTMLNode
from text_node_funcs import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return list(filter(lambda item: item != "", list(map(lambda item: item.strip(), markdown.split("\n\n")))))

def block_to_block_type(block):
    if re.match(r"^#{1,6} .*", block):
        return BlockType.HEADING
    elif re.match(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    elif re.match(r"^(>.*\n*)+$", block):
        return BlockType.QUOTE
    elif re.match(r"^(- .*\n*)+$", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^(\d\. .*\n*)+$", block) and all(list(map(lambda item: int(item[1][0]) == item[0] + 1, enumerate(block.split("\n"))))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                header_num = len(block.split(" ")[0])
                block_nodes.append(ParentNode(f"h{header_num}", text_to_children(block[header_num + 1:]), None))
            case BlockType.CODE:
                block_nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(block[4:len(block) - 3], TextType.CODE, None))], None))
            case BlockType.QUOTE:
                block_nodes.append(ParentNode("blockquote", text_to_children(re.sub(r"^>|\n>|\n", "", block).strip()), None))
            case BlockType.UNORDERED_LIST:
                list_nodes = []
                for line in block.split("\n"):
                    list_nodes.append(ParentNode("li", text_to_children(line[2:]), None))
                block_nodes.append(ParentNode("ul", list_nodes, None))
            case BlockType.ORDERED_LIST:
                list_nodes = []
                for line in block.split("\n"):
                    list_nodes.append(ParentNode("li", text_to_children(line[3:]), None))
                block_nodes.append(ParentNode("ol", list_nodes, None))
            case BlockType.PARAGRAPH:
                block_nodes.append(ParentNode("p", text_to_children(block.replace("\n", " ")), None))
            case _:
                pass
    return ParentNode("div", block_nodes, None)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes