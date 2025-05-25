import os
import sys
import shutil
from textnode import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    """Generate a single HTML page from a markdown file"""
    print(f"Processing markdown file: {from_path} -> {dest_path}")
    dest_path = os.path.splitext(dest_path)[0] + '.html'
    print(f"Final HTML path: {dest_path}")
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"Creating directory: {os.path.dirname(dest_path)}")
    
    with open(from_path) as f:
        markdown_content = f.read()
    with open(template_path) as f:
        template = f.read()
    
    title = extract_title(markdown_content)
    html_node = markdown_to_html_node(markdown_content)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())
    
    # Replace base path references
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')
    
    with open(dest_path, 'w') as f:
        f.write(html)
    print(f"Written file: {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"\nScanning directory: {dir_path_content}")
    
    for entry in os.scandir(dir_path_content):
        rel_path = os.path.relpath(entry.path, dir_path_content)
        dest_path = os.path.join(dest_dir_path, rel_path)
        
        print(f"Entry path: {entry.path}")
        print(f"Relative path: {rel_path}")
        print(f"Destination path: {dest_path}")
        
        if entry.is_file() and entry.name.endswith('.md'):
            generate_page(entry.path, template_path, dest_path, basepath)
                
        elif entry.is_dir():
            print(f"Entering directory: {entry.path}")
            new_dest_path = os.path.join(dest_dir_path, rel_path)
            generate_pages_recursive(entry.path, template_path, new_dest_path, basepath)


def copy_static_files(src_dir, dest_dir):
    """Copy all static files from src_dir to dest_dir"""
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)
    print(f"Copied static files from {src_dir} to {dest_dir}")


def main():
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    os.makedirs("docs", exist_ok=True)
    
    # Copy static files first
    copy_static_files("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()