import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive


def main() -> None:
    basepath = "./"
    if not sys.argv:
        basepath = sys.argv[1]

    dir_path_static = "./static"
    content_dir = os.path.join(basepath, "content")
    #public_dir = os.path.join(basepath, "public")
    public_dir = os.path.join(basepath, "doc")

    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, public_dir)

    # generate_page("./content/index.md", "template.html", "./public/index.html")
    # generate_page("./content/blog/glorfindel/index.md", "template.html", "./public/blog/glorfindel/index.html")
    # generate_page("./content/blog/tom/index.md", "template.html", "./public/blog/tom/index.html")
    # generate_page("./content/blog/majesty/index.md", "template.html", "./public/blog/majesty/index.html")
    # generate_page("./content/contact/index.md", "template.html", "./public/contact/index.html")

    generate_pages_recursive(content_dir, "template.html", public_dir)





if __name__ == "__main__":
    main()