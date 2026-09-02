from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"                 #paragraph
    HEADING = "heading"                     #heading
    CODE = "code"                           #code
    QUOTE = "quote"                         #quote
    ULIST = "unordered_list"       #unordered list
    OLIST = "ordered_list"           #ordered list

def markdown_to_blocks(markdown) -> list[str]:
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if line.strip() != "":
            blocks.append(line.strip())
    return blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            child_node = text_to_children(block)
            children_nodes.append(ParentNode(tag="p", children=child_node))
        elif block_type == BlockType.HEADING:
            level = re.match(r"^#+", block).group(0).count("#")
            child_node = text_to_children(block[level + 1:].strip())
            children_nodes.append(ParentNode(tag=f"h{level}", children=child_node))
        elif block_type == BlockType.CODE:
            code_lines = block.split("\n")[1:-1]
            code_content = "\n".join(code_lines) + "\n"
            child_node = [text_node_to_html_node(TextNode(code_content, TextType.CODE))]
            children_nodes.append(ParentNode(tag="pre", children=child_node))
        elif block_type == BlockType.QUOTE:
            quote_lines = [line[1:].strip() for line in block.split("\n")]
            quote_content = "\n".join(quote_lines)
            child_node = text_to_children(quote_content)
            children_nodes.append(ParentNode(tag="blockquote", children=child_node))
        elif block_type == BlockType.ULIST:
            list_items = [line[2:].strip() for line in block.split("\n")]
            child_nodes = [text_to_children(item) for item in list_items]
            list_children = [ParentNode(tag="li", children=child) for child in child_nodes]
            children_nodes.append(ParentNode(tag="ul", children=list_children))
        elif block_type == BlockType.OLIST:
            list_items = [line[line.index(".") + 1:].strip() for line in block.split("\n")]
            child_nodes = [text_to_children(item) for item in list_items]
            list_children = [ParentNode(tag="li", children=child) for child in child_nodes]
            children_nodes.append(ParentNode(tag="ol", children=list_children))
    return ParentNode(tag="div", children=children_nodes)

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes
