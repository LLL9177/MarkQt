# MarkQt

MarkQt is a small, focused markup parser that converts a simple bracket-style custom markup into HTML suitable for display in Qt-based text widgets. It's designed to be lightweight and easy to extend with custom components.

**Highlights**

- Minimal, readable markup for headers, paragraphs and inline styling
- Produces HTML safe for display in Qt `QTextBrowser`/`QTextEdit`
- Extensible components system for custom behaviors (e.g., window title)

## Supported tags

The parser recognizes a concise set of tags. Example mappings:

- `/#` → `<h1>`
- `/#2` → `<h2>`
- `/#3` → `<h3>`
- `/p` → `<p>`
- `/b` → `<b>`
- `/i` → `<i>`
- `/ult` → `<u>`
- `/t` → plain text (raw)
- `/Title` → special component that sets the application window title

Line breaks inside blocks are converted to `<br>`.

## Syntax rules

- Blocks use the form: `/tag { content }` and the content must be inside the braces.

Example:

```
/Title { My Document }
/# { Welcome }

/p {
    This is a paragraph with /i { italic text }
}
```

## Quickstart

Install runtime dependencies (PySide6 is required for the GUI renderer):

```bash
python -m pip install -r ./MarkQt/requirements.txt
```

Install the project itself as module

```bash
python -m pip install ./MarkQt
```

Create a file with your markup. You can call it whatever you want.
Now import and call the `render` function from `markqt.renderer`

```python
from markqt.renderer import render

render("./filename.txt")
```

## Components and customization

If you want, you can add custom components (I know i stole it from react). Simply pass your object with the components as a second parameter to a `render` function:

```python
def print_hello(*args, **kwargs):
  print("hello world")

render("./filename.txt", {
  "PrintHello": print_hello
})
```

When implementing component handlers, accept `*args` and `**kwargs` to keep the signature flexible.

You can also accept children and browser for more functionality

```python 
def my_function(children, browser, *args, **kwargs):
  browser.setWindowTitle(children)
  print(children)
```

As you may've guessed, children is what you put between the brackets

Also, unlike the built-in Title component, Whatever you put into your custom components as children, it will be displayed.
I don't even know why Title component doesn't display anything bro
It's not a bug. It's a feature.

## Project layout

```
MarkQt/
├── src/markqt/
│   ├── parser/parser.py    # Main parser
│   ├── components.py       # Component handlers
│   └── renderer.py         # Minimal Qt renderer demo
├── example.txt
├── requirements.txt
└── README.md
```

## Limitations & notes

- The parser expects well-formed blocks; unclosed scopes will raise errors.
- Nested block syntax has restrictions (see examples) — place nested block openings on their own lines.

## License

This project is released under the MIT License. See the `LICENSE` file for details.
