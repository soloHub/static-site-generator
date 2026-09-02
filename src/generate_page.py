import re
import os
from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

# def alt(markdown: str) -> str:
#     level = re.match(r"^#+", markdown).group(0).count("#")
#     if level != 1:
#         raise Exception("No Title '# Title'")
#     return markdown[2:].strip()

def extract_title(markdown: str) -> str:
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = re.search(r'<h1>(.*?)</h1>', html).group(1)
    if title is None:
        raise Exception("No Title '# Title'")
    return title

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as md_file:
        # Read everything into a single string variable
        markdown_content = md_file.read()
    md_file.close()
    
    with open(template_path, 'r', encoding='utf-8') as tp_file:
        template_content = tp_file.read()
    tp_file.close()
    
    html_str = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    
    template_content_edited = template_content.replace("{{ Title }}", title)
    template_content_edited = template_content_edited.replace("{{ Content }}", html_str)

    template_content_edited = template_content_edited.replace('href="/', f'href="{basepath}')
    template_content_edited = template_content_edited.replace('src="/', f'src="{basepath}')


    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'w', encoding='utf-8') as web_file:
        web_file.write(template_content_edited)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path:str, basepath: str) -> None:
    for filename in os.listdir(dir_path_content):
        dir_file = os.path.join(dir_path_content, filename)

        if os.path.isfile(dir_file):
            filename_ext_htm = filename.replace('.md', '.html')
            dest_file = os.path.join(dest_dir_path, filename_ext_htm)
            generate_page(dir_file, template_path, dest_file, basepath)
        else:
            dest_file = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(dir_file, template_path, dest_file, basepath)