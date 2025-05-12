from textnode import TextNode, TextType
from generation_helpers import generate_page, generate_pages_recursive

import os
import re
import shutil
import sys

def static_to_public(path:str, first_run: bool):
    #get cwd
    cwd = os.path.abspath(os.getcwd())
    #generate public path
    public_path = os.path.join(cwd, "docs")
    # delete public content
    if first_run:
        print("deleting public dir")
        shutil.rmtree(public_path, True)
    #check if public path exists
    if not os.path.exists(public_path):
        print("creating public path")
        os.mkdir(public_path)
    #start static recursion
    path_to_analyze = os.path.join(cwd, path)
    print(f"analyzing {path_to_analyze}")
    path_entries = os.listdir(path_to_analyze)
    for entry in path_entries:
        # create public analog path
        public_analog = os.path.join(public_path, entry)
        # check if it is a file or a directory
        if not re.search(r"\w[.]\w", entry):
            if not os.path.exists(public_analog):
                print(f"creating public analog: {public_analog}")
                os.mkdir(public_analog)
            static_to_public(os.path.join(path_to_analyze, entry), False)
        else:
            print(f"copying file {entry}")
            shutil.copy(os.path.join(path_to_analyze, entry), re.sub(r"\/static(?:$|\/)", "/docs/", path_to_analyze))

def main():
    print(sys.argv)
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = ""
    static_to_public("static", True)
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
