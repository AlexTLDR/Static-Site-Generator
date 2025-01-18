import os
import shutil
from textnode import TextNode, TextType

def copy_directory(src_dir, dst_dir):
    # Remove destination directory if it exists
    if os.path.exists(dst_dir):
        print(f"Removing existing directory: {dst_dir}")
        shutil.rmtree(dst_dir)
    
    # Create destination directory
    print(f"Creating directory: {dst_dir}")
    os.mkdir(dst_dir)
    
    # Walk through source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Copying directory: {src_path} -> {dst_path}")
            copy_directory(src_path, dst_path)

def main():
    copy_directory("static", "public")

if __name__ == "__main__":
    main()
