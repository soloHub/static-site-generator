import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("All elements in old_nodes must be instances of TextNode.")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_parts = node.text.split(delimiter)
        if len(node_parts) % 2 == 0:
            raise ValueError("Delimiter must appear an even number of times in the text.")
        for i, part in enumerate(node_parts):
            if part == "":
                continue
            if (i+1) % 2 != 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("All elements in old_nodes must be instances of TextNode.")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        parts = re.split(image_pattern, node.text)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 3 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            elif i % 3 == 1:
                alt_text = part
            elif i % 3 == 2:
                url = part
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("All elements in old_nodes must be instances of TextNode.")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        parts = re.split(link_pattern, node.text)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 3 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            elif i % 3 == 1:
                link_text = part
            elif i % 3 == 2:
                url = part
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    formatted_text = text.replace("\n", " ")
    node = TextNode(formatted_text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
