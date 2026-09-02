import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive


def main() -> None:
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    dir_path_static = "./static"
    content_dir = "./content"
    public_dir = "./docs"

    print("Deleting Docs directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, public_dir)

    generate_pages_recursive(content_dir, "template.html", public_dir, basepath)





if __name__ == "__main__":
    main()