from enum import Enum
import re

from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return(
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        splits = old_node.text.split(delimiter)
        if len(splits) % 2 == 0:
            new_nodes.append(old_node)
            continue
            
        for i in range(len(splits)):
            if splits[i] == "":
                if i == 0 or i == len(splits) - 1:
                    new_nodes.append(TextNode("", TextType.TEXT))
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splits[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(splits[i], text_type))
                
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        for alt_text, url in images:
            parts = current_text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            current_text = parts[1]
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        for anchor_text, url in links:
            parts = current_text.split(f"[{anchor_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            current_text = parts[1]
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    # Check for heading - match 1-6 # followed by space
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        if block[block.find("#"):].startswith((" ")):
            return "heading"
            
    # Check for code block - starts and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return "code"
        
    # Check for quote block - every line starts with >
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return "quote"
        
    # Check for unordered list - every line starts with * or -
    if all(line.strip().startswith(("* ", "- ")) for line in lines):
        return "unordered_list"
        
    # Check for ordered list - lines start with number. space
    if all(line.strip()[0].isdigit() and line.strip()[1:].startswith(". ") for line in lines):
        numbers = [int(line.strip().split(".")[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return "ordered_list"
            
    # Default case - paragraph
    return "paragraph"

def text_to_children(text):
    """Convert text with inline markdown to HTMLNode children"""
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def create_paragraph(text):
    return HTMLNode("p", None, text_to_children(text))

def create_heading(text):
    level = text.count("#")
    content = text[level:].strip()
    return HTMLNode(f"h{level}", None, text_to_children(content))

def create_code_block(text):
    code = text.strip().strip("```")
    return HTMLNode("pre", None, [HTMLNode("code", None, [LeafNode(code)])])

def create_quote(text):
    lines = [line.strip("> ").strip() for line in text.split("\n")]
    content = " ".join(lines)
    return HTMLNode("blockquote", None, text_to_children(content))

def create_unordered_list(text):
    items = [line.strip("* ").strip("- ") for line in text.split("\n")]
    children = [
        HTMLNode("li", None, text_to_children(item))
        for item in items
    ]
    return HTMLNode("ul", None, children)

def create_ordered_list(text):
    items = [line.split(". ", 1)[1] for line in text.split("\n")]
    children = [
        HTMLNode("li", None, text_to_children(item))
        for item in items
    ]
    return HTMLNode("ol", None, children)

def markdown_to_html_node(markdown):
    """Convert a markdown document to a single HTMLNode"""
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "paragraph":
            children.append(create_paragraph(block))
        elif block_type == "heading":
            children.append(create_heading(block))
        elif block_type == "code":
            children.append(create_code_block(block))
        elif block_type == "quote":
            children.append(create_quote(block))
        elif block_type == "unordered_list":
            children.append(create_unordered_list(block))
        elif block_type == "ordered_list":
            children.append(create_ordered_list(block))
            
    return HTMLNode("div", None, children)
