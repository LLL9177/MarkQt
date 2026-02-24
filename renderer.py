from parser.parser import parser, parse_keywords, get_blocks
from PySide6.QtWidgets import QApplication, QTextBrowser, QMainWindow
from components import components
import json
import sys

def render():
    def load_env(file_name):
        with open(file_name) as f:
            file = f.read()
            return json.loads(file)

    def get_initial_text():
        with open("./example.txt") as f:
            return f.read()
        
    def find_components(blocks, keywords):
        env = load_env("./env.json")
        components = []
        components_blocks = []
        j = 0
        for kw in keywords:
            kw = kw[1:].strip()
            if kw in env["components"]:
                if kw != '}':
                    block = blocks[j]
                    j += 1   # advance ONLY when block is consumed
                else:
                    block = None

                components.append(kw)
                components_blocks.append(block)
        
        return components, components_blocks

    def execute_components(comps, children, *args, **kwargs):
        for i in range(len(comps)):
            components[comps[i]](children[i], *args, **kwargs)
        
        return 0

    parsed_text = parser("./example.txt")
    initial_text = get_initial_text()

    lines = initial_text.split('\n')
    keywords = parse_keywords(lines)
    blocks = get_blocks(initial_text)
    comps, children = find_components(blocks, keywords)

    app = QApplication(sys.argv)

    browser = QTextBrowser()
    browser.resize(800, 600)
    browser.setHtml(parsed_text)
    execute_components(comps, children, browser)

    browser.show()
    sys.exit(app.exec())