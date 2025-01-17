import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
