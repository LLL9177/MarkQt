# MarkQt

MarkQt is a small, focused markup parser that converts a simple bracket-based custom markup into HTML. It's intended as a lightweight way to write structured documents with headers, paragraphs and inline formatting, and to render them in a minimal Qt renderer.

**Key points**
- Simple, human-readable markup
- Produces HTML output suitable for display in a Qt text widget
- Supports basic inline formatting and nested blocks

## Supported tags

The parser recognizes the following tags (tag → output):

- `/#` → `<h1>`
- `/#2` → `<h2>`
- `/#3` → `<h3>`
- `/p` → `<p>`
- `/b` → `<b>`
- `/i` → `<i>`
- `/ult` → `<u>`
- `/t` → plain text
- `/Title` → special: sets application window title (handled by `components`)

Line breaks inside blocks are converted to `<br>`.

## Syntax rules

- Blocks use the form: `/tag { content }` and content must be placed inside the braces.
- Text outside of any block is ignored by the parser.
- Do not start multiple block openings on the same line; nested blocks should be started on their own lines inside the parent block.

Example:

```
/Title { My Document }
/# { Welcome }

/p {
    This is a paragraph with /i { italic text }
}
```

## Running

Install Python requirements (if needed):

```bash
python -m pip install -r Markqt/requirements.txt
```

Run the renderer which uses Qt to display the parsed HTML:

```bash
python Markqt/renderer.py
```

Or parse a file directly from Python:

```python
from MarkQt.parser.parser import parser
html = parser("./MarkQt/example.txt")
print(html)
```

or create your own file that will call renderer:
```python
from MarkQt.renderer import render
render()
```

## Renderer and components

- `renderer.py` demonstrates loading `example.txt`, parsing it and showing the resulting HTML in a `QTextBrowser`.
- Custom behaviors (non-HTML tags) can be implemented as components. See `components.py` and `env.json`:
  - `components.py` maps component names (like `Title`) to functions that receive the block content and the Qt widget. Note that your function must contain args and kwargs as parameters if you don't want to get an error.
  - `env.json` lists active components by name.

## Project layout

```
MarkQt/
├── parser/
│   ├── parser.py       # Main parsing logic
│   ├── rules.txt       # Tag reference (informational)
│   └── __init__.py
├── components.py       # Example component handlers
├── renderer.py         # Minimal Qt renderer demo
├── example.txt         # Sample markup
├── env.json            # Which components are enabled
└── README.md
```

## Notes and limitations

- The parser expects well-formed blocks and will raise if scopes are not closed.
- The current syntax has some restrictions (e.g. starting multiple blocks on one line). These are documented above.
