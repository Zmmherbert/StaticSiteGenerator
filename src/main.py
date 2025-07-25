from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_node_funcs import *
from copy_static import copy_static
from generate_page import *
import os
import sys

def main():
    basepath = "/"
    if sys.argv[1]:
        basepath = sys.argv[1]
    
    copy_static("docs/")
    cwd = os.getcwd()
    generate_pages_recursive(os.path.join(cwd, "content/"), os.path.join(cwd, "template.html"), os.path.join(cwd, "docs/"), basepath)

main()