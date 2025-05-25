import os
import shutil
from textnode import markdown_to_html_node, extract_title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"\nScanning directory: {dir_path_content}")
    
    for entry in os.scandir(dir_path_content):
        rel_path = os.path.relpath(entry.path, dir_path_content)
        dest_path = os.path.join(dest_dir_path, rel_path)
        
        print(f"Entry path: {entry.path}")
        print(f"Relative path: {rel_path}")
        print(f"Destination path: {dest_path}")
        
        if entry.is_file() and entry.name.endswith('.md'):
            print(f"Processing markdown file: {entry.path} -> {dest_path}")
            dest_path = os.path.splitext(dest_path)[0] + '.html'
            print(f"Final HTML path: {dest_path}")
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            print(f"Creating directory: {os.path.dirname(dest_path)}")
            
            with open(entry.path) as f:
                markdown_content = f.read()
            with open(template_path) as f:
                template = f.read()
            
            title = extract_title(markdown_content)
            html_node = markdown_to_html_node(markdown_content)
            html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())
            
            with open(dest_path, 'w') as f:
                f.write(html)
            print(f"Written file: {dest_path}")
                
        elif entry.is_dir():
            print(f"Entering directory: {entry.path}")
            new_dest_path = os.path.join(dest_dir_path, rel_path)
            generate_pages_recursive(entry.path, template_path, new_dest_path)


def copy_static_files(src_dir, dest_dir):
    """Copy all static files from src_dir to dest_dir"""
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)
    print(f"Copied static files from {src_dir} to {dest_dir}")


def main():
    os.makedirs("public", exist_ok=True)
    
    # Copy static files first
    copy_static_files("static", "public")

    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
