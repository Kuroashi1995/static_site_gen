import os
import re
from html_helpers import markdown_to_html_node, extract_title

def generate_page(from_path: str, template_path: str, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    cwd = os.path.abspath(os.getcwd())
    abs_md_path = os.path.join(cwd, from_path)
    abs_template_path = os.path.join(cwd, template_path)
    abs_dest_path = os.path.join(cwd, dest_path)

    # Read md content
    with open(abs_md_path) as mdf:
        md = mdf.read()
    with open(abs_template_path) as tf:
        template = tf.read()

    # Get html string from md
    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    new_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    if not os.path.exists(abs_dest_path.replace("/index.html","")):
        print("Creating destination path")
        os.mkdir(abs_dest_path)
    with open(abs_dest_path, "x") as df:
        df.write(new_template)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    cwd = os.path.abspath(os.getcwd())
    current_dir = os.path.join(cwd, dir_path_content)
    entries = os.listdir(current_dir)
    print(entries)
    for entry in entries:
        if not re.compile(r"\w[.]\w").search(entry):
            path_to_create = os.path.join(cwd, os.path.join(dest_dir_path, entry))
            print(f"creating path: {path_to_create}")
            os.mkdir(path_to_create)
            print("going into path")
            generate_pages_recursive(os.path.join(current_dir, entry), template_path, dest_dir_path + "/" + entry)
        else:
            print("generating page")
            generate_page(os.path.join(dir_path_content, entry), template_path, os.path.join(dest_dir_path, entry.replace(".md", ".html")))
