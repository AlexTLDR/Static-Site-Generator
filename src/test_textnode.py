import unittest

from textnode import *



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_equal_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        node2 = TextNode("", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_url_none_vs_url_set(self):
        node = TextNode("Same text", TextType.LINK)
        node2 = TextNode("Same text", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_different_type_same_url(self):
        node = TextNode("Same text", TextType.LINK, "https://example.com")
        node2 = TextNode("Same text", TextType.TEXT, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_none_url_equality(self):
        node = TextNode("Same text", TextType.LINK)
        node2 = TextNode("Same text", TextType.LINK)
        self.assertEqual(node, node2)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_multiple(self):
        nodes = [
            TextNode("Over the ", TextType.TEXT),
            TextNode("rainbow", TextType.BOLD),
            TextNode(" and through the `code block` is my *italic* text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Over the ", TextType.TEXT),
                TextNode("rainbow", TextType.BOLD),
                TextNode(" and through the `code block` is my ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_no_split(self):
        node = TextNode("This is text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [TextNode("This is text without delimiters", TextType.TEXT)]
        )

    def test_split_nodes_delimiter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("", TextType.TEXT)])

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png")
            ]
        )

    def test_extract_markdown_images_empty(self):
        text = "This is text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.boot.dev) and [another link](https://www.github.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.boot.dev"),
                ("another link", "https://www.github.com")
            ]
        )

    def test_extract_markdown_links_empty(self):
        text = "This is text with no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_mixed(self):
        text = "This has ![image](https://imgur.com) and [link](https://boot.dev)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://imgur.com")])
        self.assertEqual(extract_markdown_links(text), [("link", "https://boot.dev")])

    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" in it", TextType.TEXT),
            ]
        )

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is text with [link1](https://boot.dev) and [link2](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://github.com"),
            ]
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text with no links in it", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_link_multiple_nodes(self):
        nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and a [link](https://boot.dev) in it", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" in it", TextType.TEXT),
            ]
        )

    def test_split_nodes_image_basic(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/img.png) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" in it", TextType.TEXT),
            ]
        )

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "![img1](https://example.com/1.png) and ![img2](https://example.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
            ]
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text with no images in it", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_image_multiple_nodes(self):
        nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ![img](https://example.com/img.png) in it", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" in it", TextType.TEXT),
            ]
        )

def test_text_to_textnodes_empty(self):
    nodes = text_to_textnodes("")
    self.assertEqual(nodes, [TextNode("", TextType.TEXT)])

def test_text_to_textnodes_plain_text(self):
    nodes = text_to_textnodes("Just plain text")
    self.assertEqual(nodes, [TextNode("Just plain text", TextType.TEXT)])

def test_text_to_textnodes_bold_only(self):
    nodes = text_to_textnodes("**bold text**")
    self.assertEqual(nodes, [TextNode("bold text", TextType.BOLD)])

def test_text_to_textnodes_multiple_bold(self):
    nodes = text_to_textnodes("**first** normal **second**")
    self.assertEqual(
        nodes,
        [
            TextNode("first", TextType.BOLD),
            TextNode(" normal ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
        ]
    )

def test_text_to_textnodes_nested_formatting(self):
    nodes = text_to_textnodes("**bold with *italic* inside**")
    self.assertEqual(
        nodes,
        [
            TextNode("bold with ", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode(" inside", TextType.BOLD),
        ]
    )

def test_text_to_textnodes_multiple_types(self):
    nodes = text_to_textnodes("`code` *italic* **bold** [link](https://example.com)")
    self.assertEqual(
        nodes,
        [
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
    )

def test_text_to_textnodes_images_and_links(self):
    nodes = text_to_textnodes("![alt text](image.jpg) and [link text](https://example.com)")
    self.assertEqual(
        nodes,
        [
            TextNode("alt text", TextType.IMAGE, "image.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "https://example.com"),
        ]
    )

def test_text_to_textnodes_complex_markdown(self):
    text = """This is a **complex** test with
    *italic*, `code`, ![image](test.png) and [link](https://test.com)
    across multiple lines"""
    nodes = text_to_textnodes(text)
    self.assertEqual(
        nodes,
        [
            TextNode("This is a ", TextType.TEXT),
            TextNode("complex", TextType.BOLD),
            TextNode(" test with\n    ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "test.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://test.com"),
            TextNode("\n    across multiple lines", TextType.TEXT),
        ]
    )

def test_markdown_to_blocks(self):
    markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item  
* This is another list item"""

    blocks = markdown_to_blocks(markdown)
    self.assertEqual(
        blocks,
        [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
    )

def test_block_to_block_type(self):
    self.assertEqual(block_to_block_type("# Heading"), "heading")
    self.assertEqual(block_to_block_type("### Heading 3"), "heading")
    
    self.assertEqual(
        block_to_block_type("```\ncode block\nmore code\n```"), 
        "code"
    )
    
    self.assertEqual(
        block_to_block_type("> quote\n> more quote\n> final quote"), 
        "quote"
    )
    
    self.assertEqual(
        block_to_block_type("* list item\n* another item\n* final item"), 
        "unordered_list"
    )
    
    self.assertEqual(
        block_to_block_type("- list item\n- another item\n- final item"), 
        "unordered_list"
    )
    
    self.assertEqual(
        block_to_block_type("1. first item\n2. second item\n3. third item"), 
        "ordered_list"
    )
    
    self.assertEqual(
        block_to_block_type("Regular paragraph text with **bold** and *italic*"), 
        "paragraph"
    )

def test_block_to_block_type_invalid_heading(self):
    self.assertEqual(block_to_block_type("#Invalid heading"), "paragraph")
    
def test_block_to_block_type_invalid_ordered_list(self):
    self.assertEqual(
        block_to_block_type("1. first\n3. second\n4. third"), 
        "paragraph"
    )

def test_block_to_block_type_mixed_list_markers(self):
    self.assertEqual(
        block_to_block_type("* first\n- second"), 
        "unordered_list"
    )



if __name__ == "__main__":
    unittest.main()