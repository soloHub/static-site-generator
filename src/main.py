import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # generate_page("./content/index.md", "template.html", "./public/index.html")
    # generate_page("./content/blog/glorfindel/index.md", "template.html", "./public/blog/glorfindel/index.html")
    # generate_page("./content/blog/tom/index.md", "template.html", "./public/blog/tom/index.html")
    # generate_page("./content/blog/majesty/index.md", "template.html", "./public/blog/majesty/index.html")
    # generate_page("./content/contact/index.md", "template.html", "./public/contact/index.html")
    
    generate_pages_recursive("./content", "template.html", "./public")





if __name__ == "__main__":
    main()