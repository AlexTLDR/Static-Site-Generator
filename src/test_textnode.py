import unittest

from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    text_node_to_html_node,
    extract_markdown_images,
    extract_markdown_links
)


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



if __name__ == "__main__":
    unittest.main()