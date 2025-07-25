from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_node_funcs import *
from copy_static import copy_static
from generate_page import *
import os

def main():
    copy_static()
    cwd = os.getcwd()
    generate_pages_recursive(os.path.join(cwd, "content/"), os.path.join(cwd, "template.html"), os.path.join(cwd, "public/"))

main()