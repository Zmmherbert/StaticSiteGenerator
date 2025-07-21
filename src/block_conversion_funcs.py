from enum import Enum
import re

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
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                pass
            case BlockType.CODE:
                pass
            case BlockType.QUOTE:
                pass
            case BlockType.UNORDERED_LIST:
                pass
            case BlockType.ORDERED_LIST:
                pass
            case BlockType.PARAGRAPH:
                pass
            case _:
                pass