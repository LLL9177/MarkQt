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

def add_custom_componentsB(components):
    global types
    types.update(components)

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


def _sorted_type_keys():
    return sorted(types.keys(), key=len, reverse=True)


def _parse_recursive(text, pos=0, end_char=None):
    n = len(text)
    parts = []
    keys = _sorted_type_keys()

    while pos < n:
        if end_char is not None and text[pos] == end_char:
            return ''.join(parts), pos + 1

        matched = False

        for key in keys:
            if text.startswith(key, pos):
                # handle explicit newline token
                if key == '\\n':
                    parts.append(types[key])
                    pos += len(key)
                    matched = True
                    break

                next_pos = pos + len(key)
                # only treat as a tag when followed by an opening brace,
                # allowing optional whitespace between key and '{'
                look_pos = next_pos
                while look_pos < n and text[look_pos].isspace():
                    look_pos += 1
                if look_pos < n and text[look_pos] == '{':
                    pos = look_pos + 1  # skip key, optional spaces and '{'
                    inner, pos = _parse_recursive(text, pos, '}')
                    tag = types[key]
                    # trim a single leading newline + indentation and a single trailing newline + indentation
                    if inner.startswith('\n'):
                        i = 1
                        while i < len(inner) and inner[i] in (' ', '\t', '\r'):
                            i += 1
                        inner = inner[i:]
                    if inner.endswith('\n'):
                        j = len(inner) - 1
                        while j - 1 >= 0 and inner[j-1] in (' ', '\t', '\r'):
                            j -= 1
                        inner = inner[:j]
                    parts.append(f"<{tag}>{inner}</{tag}>")
                    matched = True
                    break

        if matched:
            continue

        # no special token matched; copy character
        parts.append(text[pos])
        pos += 1

    if end_char is not None:
        raise Exception("Forgot to close a scope")

    return ''.join(parts), pos


def parse_text_to_html(text):
    out, _ = _parse_recursive(text, 0, None)

    def _convert_newlines_outside_tags(s):
        res = []
        cur = []
        inside_tag = False
        i = 0
        n = len(s)

        while i < n:
            ch = s[i]
            if ch == '<':
                inside_tag = True
                cur.append(ch)
                i += 1
            elif ch == '>':
                inside_tag = False
                cur.append(ch)
                i += 1
            elif ch == '\n':
                if inside_tag:
                    cur.append(ch)
                    i += 1
                else:
                    # look ahead: if next non-space char is '<', treat this newline as formatting
                    j = i + 1
                    while j < n and s[j] in (' ', '\t', '\r'):
                        j += 1

                    if j < n and s[j] == '<':
                        # drop the newline and any indentation spaces
                        i = j
                        # also trim trailing spaces from current buffer
                        while cur and cur[-1].isspace():
                            cur.pop()
                        continue

                    line = ''.join(cur)
                    if line.strip() != '':
                        res.append(line.rstrip())
                        res.append("<br>\n")
                    cur = []
                    i += 1
            else:
                cur.append(ch)
                i += 1

        if cur:
            res.append(''.join(cur))

        return ''.join(res)

    return _convert_newlines_outside_tags(out)

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
            if scope == 0:
                raise Exception("Extra closing brace detected")
            scope -= 1
            if scope == 0:
                # Only collect blocks from completed root-level scopes
                for value in scopes.values():
                    new_value = strip_keywords(value)
                    blocks.append(new_value)
                scopes = {}
                reading = False
        else:
            if reading and scope > 0:
                # Only accumulate text inside a block (scope > 0)
                scopes[str(scope)] += c

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
        ret = parse_text_to_html(text)

    return ret