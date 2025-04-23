# PDF Injector

A tool for injecting invisible text into PDF files. The text is invisible to human viewers but can be detected by text extraction tools and LLMs.

## Installation

### From PyPI

```bash
pip install pdf-injector
```

### From Source

```bash
git clone https://github.com/larsyencken/pdf-injector.git
cd pdf-injector
make .venv
```

## Development

This project uses:
- `ruff` for linting and formatting
- `pyright` for type checking
- `pytest` for unit testing

### Common Tasks

```bash
# Set up the development environment
make .venv

# Format code
make tidy

# Check formatting
make checkformatting

# Run unit tests
make unittest

# Run type checking
make typecheck

# Run all checks
make test

# Clean up environment
make clean
```

## Usage

### When installed from PyPI

```bash
pdf-injector input.pdf output.pdf "Text to inject invisibly"
```

### When running from source

```bash
python main.py input.pdf output.pdf "Text to inject invisibly"
```

### Arguments:

- `input_pdf`: Path to the existing PDF file
- `output_pdf`: Path where the modified PDF will be saved
- `text`: Text to inject (will be invisible to humans but readable by machines)

## How It Works

This tool uses Text Rendering Mode 3 in the PDF specification, which renders text as invisible but still includes it in the document content stream. This means:

1. The text is not visible when viewing the PDF
2. The text is still part of the document structure
3. Text extraction tools and LLMs can still "read" the invisible text

## Technical Details

- Uses PyPDF for reading/writing PDF files
- Uses ReportLab for creating the invisible text layer
- Applies the invisible text to each page of the input PDF

## Changelog

### 0.1.1 (2025-04-23)
- Improved text rendering mode implementation for true invisibility
- Added CI workflow for automated testing
- Fixed package installation and entry point configuration
- Added distribution and publishing capabilities 
- Added command-line tool with pip installation support

### 0.1.0 (2025-04-23)
- Initial implementation of PDF text injector
- Support for injecting invisible text into PDF files
- Basic test suite and documentation