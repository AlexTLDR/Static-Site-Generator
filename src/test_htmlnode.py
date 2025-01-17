import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode(tag="p", props={"class": "text-center"})
        self.assertEqual(node.props_to_html(), ' class="text-center"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.example.com",
                "target": "_blank",
                "class": "link"
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.example.com" target="_blank" class="link"'
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_tag(self):
        node = LeafNode("p", "This is a paragraph of text")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text</p>")

    def test_leaf_node_with_tag_and_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_node_without_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ]
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]
                )
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text</p><p><i>italic text</i>Normal text</p></div>"
        )

    def test_parent_node_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Hello, world!")],
            {"class": "greeting", "id": "hello"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="greeting" id="hello">Hello, world!</div>'
        )

    def test_missing_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "Test")])

    def test_missing_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "This is a text")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<b>This is bold</b>")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<i>This is italic</i>")

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<code>This is code</code>")

    def test_text_node_to_html_node_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.example.com">Click me</a>'
        )

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://www.example.com/image.png" alt="Alt text">'
        )

    def test_text_node_to_html_node_invalid(self):
        node = TextNode("Invalid type", "invalid")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
