import unittest

from htmlnode import HTMLNode, LeafNode

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

    


if __name__ == "__main__":
    unittest.main()
