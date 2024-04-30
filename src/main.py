from textnode import TextNode
from htmlnode import HTMLNode
from markdown_blocks import markdown_to_html_node
import os
import shutil

def copy_static(src_dir, dest_dir):
    src_path = os.listdir(src_dir)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.listdir(dest_dir)
    for item in src_path:
        item_path = os.path.join(src_dir, item)
        if os.path.isfile(item_path):
            shutil.copyfile(item_path, os.path.join(dest_dir, item))
        if os.path.isdir(item_path):
            os.path.join(dest_dir+item)
            new_dest_dir = os.path.join(dest_dir, item)
            copy_static(item_path, new_dest_dir)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    updated_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(updated_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            if item.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, item[:-3]+".html")
                generate_page(item_path, template_path, dest_path)
        if os.path.isdir(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest_dir)

def main():
    generate_pages_recursive("content", "template.html", "public")
                  
if __name__ == "__main__":
    main()


