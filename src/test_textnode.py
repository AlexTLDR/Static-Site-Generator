import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()