import os

# We'll simply put <, > and </ around the name
types = {
    "/#": "h1",
    "/#2": "h2",
    "/#3": "h3",
    "/t": "text",
    "/p": "p",
    "/b": "b",
    "/i": "i",
    "/ult": "u",
    "/Title": "Title", # This is not a real html tag. Specifies window name
    '\\n': "<br>"
}

def parse_keywords(lines):
    keywords = [] # Each keyword represents a line
    for l in lines:
        if '{' in l:
            temp = ''
            index = l.index('/')
            char = l[index]
            while True:
                if char == '{': break
                temp += char
                index += 1
                char = l[index]

            keywords.append(temp)

        if '}' in l:
            keywords.append('}')
    
    return keywords

def strip_keywords(text):
    ret = text
    for key in types.keys():
        if key in ret:
            ret = ret.replace(key, '')

    return ret

def get_blocks(text):
    blocks = []
    scopes = {}
    scope = 0

    reading = False

    for i, c in enumerate(text):
        next_char = text[i + 1] if i + 1 < len(text) else None

        if c == '{':
            scope += 1
            scopes[str(scope)] = ''
            reading = True
        elif c == '}':
            scope -= 1
            if scope == 0:
                reading = False
                if next_char is not None:
                    for value in scopes.values():
                        new_value = strip_keywords(value)
                        blocks.append(new_value)

                    scopes = {}
        else:
            if reading:
                scopes[str(scope)] += c

        if next_char is None:
            for value in scopes.values():
                new_value = strip_keywords(value)
                blocks.append(new_value)

    if scope > 0:
        raise Exception("Forgot to close a scope")

    return blocks

def get_type(kw):
    return types[kw.strip()]

def render_block_text(block):
    lines = block.splitlines()
    return "<br>\n".join(line.rstrip() for line in lines if line.strip() != "")

def convert_block(block, kw):
    kw = get_type(kw)
    block = render_block_text(block)
    return f"<{kw}>\n{block}\n</{kw}>"

def open_block(block, kw):
    kw = get_type(kw)
    block = render_block_text(block)
    return f"<{kw}>\n{block}"

def convert_blocks(blocks, keywords):
    ret = ''
    is_current_child = False
    j=0
    opened_blocks = []

    for i in range(len(keywords)):
        kw = keywords[i].strip()
        next_kw = keywords[i+1] if i+1 < len(keywords) else None

        if kw != '}' and kw in types:
            block = blocks[j]
            j += 1   # advance ONLY when block is consumed
        else:
            block = None

        if next_kw == '}':
            if not is_current_child:
                if kw != '}':
                    ret += convert_block(block, kw)
        elif next_kw is not None and kw != '}':
            ret += open_block(block, kw)
            opened_blocks.append(kw)
        
        if kw in types.keys():
            is_current_child = False
        elif kw == '}' and len(opened_blocks) > 0:
            typed_kw = get_type(opened_blocks[-1])
            ret += f"</{typed_kw}>"
            is_current_child = True
            opened_blocks.pop(-1)

    return ret


def parser(file_location):
    ret = ''
    with open(file_location) as f:
        text = f.read()
        lines = text.split('\n')
        keywords = parse_keywords(lines)
        blocks = get_blocks(text)
        ret = convert_blocks(blocks, keywords)

    return ret