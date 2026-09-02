import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value="Hello", props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html(self):
        node = HTMLNode(tag="div", value="Hello", props={"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="div", value="Hello", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", value="Hello")
        self.assertEqual(node.props_to_html(), '')

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", props={"class": "my-class"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Hello, children=None, props={'class': 'my-class'})")


    def test_leaf_init(self):
        leaf = LeafNode(tag="p", value="Hello", props={"class": "my-class"})
        self.assertEqual(leaf.tag, "p")
        self.assertEqual(leaf.value, "Hello")
        self.assertEqual(leaf.children, None)
        self.assertEqual(leaf.props, {"class": "my-class"})

    def test_leaf_to_html_with_tag_value(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_tag_value_props(self):
        leaf = LeafNode(tag="p", value="Hello", props={"class": "my-class"})
        self.assertEqual(leaf.to_html(), '<p class="my-class">Hello</p>')

    def test_leaf_to_html_no_tag(self):
        leaf = LeafNode(tag=None, value="Hello")
        self.assertEqual(leaf.to_html(), 'Hello')

    def test_leaf_to_html_no_value(self):
        leaf = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_repr(self):
        leaf = LeafNode(tag="p", value="Hello", props={"class": "my-class"})
        self.assertEqual(repr(leaf), "LeafNode(tag=p, value=Hello, props={'class': 'my-class'})")


    def test_parent_init(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "my-class"})
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.value, None)
        self.assertEqual(parent.children, [child1, child2])
        self.assertEqual(parent.props, {"class": "my-class"})
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "my-class"})
        self.assertEqual(parent.to_html(), '<div class="my-class"><p>Child 1</p><p>Child 2</p></div>')

    def test_parent_to_html_no_tag(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag=None, children=[child1, child2], props={"class": "my-class"})
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_parent_to_html_no_children(self):
        parent = ParentNode(tag="div", children=None, props={"class": "my-class"})
        with self.assertRaises(ValueError):
            parent.to_html()


    def test_text_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_to_html_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_text_to_html_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_text_to_html_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_text_to_html_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://www.boot.dev/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/image.png", "alt": "This is an image text node"})    

if __name__ == '__main__':
    unittest.main()