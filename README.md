# MarkQt

A lightweight markup parser that converts a custom markup syntax into HTML. MarkQt provides a simple and intuitive way to define document structure with tags like headers, paragraphs, and text formatting.

## Features

- **Custom Markup Syntax**: Simple, readable syntax for defining document structure
- **HTML Output**: Converts markup files directly to HTML format
- **Text Formatting**: Support for bold, italic, and underlined text
- **Headers**: Multiple header levels (h1, h2, h3)
- **Paragraphs**: Block-level paragraph support
- **Flexible Nesting**: Allows nested formatting within content blocks
- Will add renderer later

## Syntax

MarkQt uses a bracket-based syntax to define content blocks:

```
/tag { content }
```

### Supported Tags

| Tag | Output | Purpose |
|-----|--------|---------|
| `/#` | `<h1>` | Header Level 1 |
| `/#2` | `<h2>` | Header Level 2 |
| `/#3` | `<h3>` | Header Level 3 |
| `/p` | `<p>` | Paragraph |
| `/b` | `<b>` | Bold text |
| `/i` | `<i>` | Italic text |
| `/ult` | `<u>` | Underlined text |
| `/t` | `<text>` | Plain text |
| `/title` | Special | Window title (not an HTML tag) |

## Usage

### Basic Example

Create a `.txt` file with MarkQt syntax:

```
/title { My Document }
/# { Welcome }

/p {
    This is a paragraph with /i { italic text }
}
```

### Text must be always wrapped in a tag
If you write anything outside of scopes (blocks if you like), it will be **ignored by the parser**.

For example:
```markup
This line is ignored...
/t {Hello world}
So is this line
```

### Can't start different blocks in one line
If you write something like this:
```markup
/t {/i {this text is italic}}
```
It wouldn't work. For it to be parsed and not ignored, you need to do this:
```markup
/t {
    /i {This text is italic}
}
```
You might've already guessed that this issue exists **because I'm lazy**. And i don't think i'll be fixing that in a closer future.

### Running the Parser

```python
from parser.parser import parser

# Parse a file and get HTML output
html = parser("./example.txt")
print(html)
```

Or use the renderer:

```bash
python renderer.py
```

## Project Structure

```
MarkQt/
├── parser/
│   ├── parser.py       # Main parsing logic
│   ├── rules.txt       # Tag definitions reference
│   └── __init__.py
├── renderer.py         # Example renderer script
├── example.txt         # Sample markup file
└── README.md          # This file
```

## Example

See `example.txt` for a complete example with quotes formatted in various ways, including nested formatting.

## License

This project is open source.
