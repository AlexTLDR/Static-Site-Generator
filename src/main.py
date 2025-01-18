import os
import shutil
from textnode import *

def copy_directory(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        print(f"Removing existing directory: {dst_dir}")
        shutil.rmtree(dst_dir)
    
    print(f"Creating directory: {dst_dir}")
    os.mkdir(dst_dir)
    
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Copying directory: {src_path} -> {dst_path}")
            copy_directory(src_path, dst_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w') as f:
        f.write(template)

def main():
    # Copy static files
    copy_directory("static", "public")
    
    # Generate index page
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )

if __name__ == "__main__":
    main()
