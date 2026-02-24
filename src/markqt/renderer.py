from .parser.parser import parser, parse_keywords, get_blocks
from PySide6.QtWidgets import QApplication, QTextBrowser
from .components import add_custom_components
import sys

def render(file_name, custom_components={}):
    components = add_custom_components(custom_components)
    print(components)

    def get_initial_text():
        with open(file_name) as f:
            return f.read()
        
    def find_components(blocks, keywords):
        kws_ret = []
        blocks_ret = []
        j = 0
        for i in range(len(keywords)):
            kw = keywords[i][1:].strip()
            if keywords[i] == '}': 
                continue
            if kw not in components.keys():
                j += 1
                continue
            kws_ret.append(kw)
            blocks_ret.append(blocks[j])
            j += 1

        return kws_ret, blocks_ret

    def execute_components(comps, children, browser, *args, **kwargs):
        for i in range(len(comps)):
            components[comps[i]](children[i], browser, *args, **kwargs)
        
        return 0

    parsed_text = parser(file_name)
    initial_text = get_initial_text()

    lines = initial_text.split('\n')
    keywords = parse_keywords(lines)
    blocks = get_blocks(initial_text)
    comps, children = find_components(blocks, keywords)

    app = QApplication(sys.argv)
    print(comps, children)

    browser = QTextBrowser()
    browser.resize(800, 600)
    browser.setHtml(parsed_text)
    execute_components(comps, children, browser)

    browser.show()
    sys.exit(app.exec())