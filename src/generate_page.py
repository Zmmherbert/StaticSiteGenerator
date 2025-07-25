from htmlnode import HTMLNode, ParentNode, LeafNode
from block_conversion_funcs import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = ""
    template_file = ""
    with open(from_path, 'r') as file:
        markdown_file = file.read()
    with open(template_path, 'r') as file:
        template_file = file.read()
    content = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", content)
    os.makedirs(dest_path[:dest_path.rfind("/")], exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(template_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, item)
        if os.path.isfile(path) and path.endswith(".md"):
            generate_page(path, template_path, os.path.join(dest_dir_path, item).replace(".md", ".html"))
        elif os.path.isdir(path):
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, item))
        else:
            raise Exception("Not a file or a directory???")