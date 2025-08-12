# Static Site Generator

A lightweight static site generator written in Python that converts Markdown files to HTML using a custom template system.

## Features

- **Markdown to HTML conversion** - Convert Markdown files to static HTML pages
- **Template system** - Use customizable HTML templates with placeholder substitution
- **Recursive directory processing** - Automatically process nested directory structures
- **Static asset copying** - Copy CSS, images, and other static files to the output directory
- **Custom Markdown parser** - Built-in parser supporting:
  - Headers (H1-H6)
  - Bold and italic text
  - Code blocks and inline code
  - Links and images
  - Lists (ordered and unordered)
  - Blockquotes
- **Flexible base path support** - Configure for different deployment scenarios
- **Local development server** - Built-in HTTP server for testing

## Project Structure

```
Static-Site-Generator/
├── src/                    # Source code
│   ├── main.py            # Main application logic
│   ├── textnode.py        # Markdown parsing and text processing
│   ├── htmlnode.py        # HTML node generation and manipulation
│   └── test_*.py          # Unit tests
├── content/               # Markdown content files
│   ├── index.md          # Home page content
│   ├── blog/             # Blog posts
│   └── contact/          # Contact pages
├── static/               # Static assets (CSS, images, etc.)
├── docs/                 # Generated HTML output
├── template.html         # HTML template with placeholders
├── build.sh             # Production build script
├── main.sh              # Development script with local server
└── test.sh              # Test runner script
```

## Requirements

- Python 3.x
- No external dependencies required

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Static-Site-Generator
   ```

2. Ensure Python 3 is installed on your system

## Usage

### Development Mode

Run the generator and start a local development server:

```bash
./main.sh
```

This will:
- Generate the static site in the `docs/` directory
- Start a local HTTP server on port 8888
- Open your browser to `http://localhost:8888`

### Production Build

Generate the site for deployment with a custom base path:

```bash
./build.sh
```

Or run manually with a custom base path:

```bash
python3 src/main.py "/your-base-path/"
```

### Custom Usage

Generate pages manually:

```bash
python3 src/main.py [base_path]
```

- `base_path` (optional): The base URL path for the site (default: "/")

## Content Creation

### Adding Pages

1. Create Markdown files in the `content/` directory
2. The first H1 header (`# Title`) will be used as the page title
3. The directory structure in `content/` will be preserved in the output

### Template Customization

Edit `template.html` to customize the HTML structure. Use these placeholders:

- `{{ Title }}` - Replaced with the page title (first H1 header)
- `{{ Content }}` - Replaced with the converted HTML content

### Static Assets

Place CSS, images, and other static files in the `static/` directory. They will be copied to the output directory during generation.

## Markdown Support

The generator supports standard Markdown syntax:

- **Headers**: `# H1`, `## H2`, `### H3`, etc.
- **Bold text**: `**bold**` or `__bold__`
- **Italic text**: `*italic*` or `_italic_`
- **Code**: `` `inline code` `` and ```code blocks```
- **Links**: `[text](url)`
- **Images**: `![alt text](url)`
- **Lists**: Both numbered and bulleted lists
- **Blockquotes**: `> quote text`

## Development

### Running Tests

Execute the test suite:

```bash
./test.sh
```

Or run manually:

```bash
python3 -m unittest discover -s src
```

### Architecture

The generator consists of two main components:

- **TextNode**: Represents parsed Markdown elements with type information
- **HTMLNode**: Generates HTML from TextNode structures

The conversion process:
1. Parse Markdown content into TextNode objects
2. Convert TextNode tree to HTMLNode tree
3. Render HTMLNode tree to HTML string
4. Apply template substitution
5. Write to output file

## Scripts

- `main.sh` - Development mode with local server
- `build.sh` - Production build with custom base path
- `test.sh` - Run unit tests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Alex Badragan