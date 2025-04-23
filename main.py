#!/usr/bin/env python3
import argparse
import os
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_invisible_text_layer(text: str, page_size=letter) -> BytesIO:
    """Create a PDF with invisible text using Text Rendering Mode 3 and transparency."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=page_size)

    # Set text rendering mode to 3 (invisible text)
    # The correct way to set text rendering mode in ReportLab
    # Using setattr to avoid type checking issues with protected attribute
    setattr(c, "_textRenderMode", 3)

    # Make the text transparent as a fail-safe
    c.setFillColorRGB(0, 0, 0, 0)
    c.setStrokeColorRGB(0, 0, 0, 0)

    # Use a common OCR-friendly font
    c.setFont("Helvetica", 10)

    # Write text
    lines = text.split("\n")
    y_position = page_size[1] - 50  # Start near top
    for line in lines:
        t = c.beginText(50, y_position)
        t.setTextRenderMode(3)  # Invisible text (no fill, no stroke)
        t.textOut(line)  # Add the text content
        c.drawText(t)  # Draw the text object to the canvas
        y_position -= 15

    c.save()
    buffer.seek(0)
    return buffer


def create_tiny_prompt_layer(page_size, text: str, font_size=4) -> BytesIO:
    """Create a PDF with tiny visible text at the bottom of the page."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=page_size)
    
    # Set a very small font size
    c.setFont("Helvetica", font_size)
    
    # Set to light gray color to be less noticeable
    c.setFillColorRGB(0.7, 0.7, 0.7)
    
    # Position at the bottom of the page with small margin
    y_position = 10  # 10 points from bottom
    
    # Draw the text
    c.drawString(10, y_position, text)
    
    c.save()
    buffer.seek(0)
    return buffer


def inject_invisible_text(
    input_pdf_path: str, output_pdf_path: str, text: str, prompt_text: str | None = None
) -> None:
    """
    Inject invisible text into an existing PDF.
    
    Args:
        input_pdf_path: Path to the input PDF file
        output_pdf_path: Path where the modified PDF will be saved
        text: Text to inject invisibly
        prompt_text: Optional tiny visible text to add at the bottom of the last page.
                    If None, no visible text is added.
    """
    # Read the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    num_pages = len(reader.pages)
    
    # Process each page
    for i, page in enumerate(reader.pages):
        # Get the original page dimensions
        page_width = page.mediabox.width
        page_height = page.mediabox.height
        page_size = (page_width, page_height)
        
        # For all pages, add invisible text
        overlay_buffer = create_invisible_text_layer(text)
        overlay_pdf = PdfReader(overlay_buffer)
        overlay_page = overlay_pdf.pages[0]
        
        # Scale the overlay to match the original page size
        overlay_page.scale_to(page_width, page_height)
        
        # Merge the invisible text overlay with the original page
        page.merge_page(overlay_page)
        
        # If this is the last page and prompt_text is provided, add tiny visible prompt
        if i == num_pages - 1 and prompt_text is not None:
            prompt_buffer = create_tiny_prompt_layer(page_size, prompt_text)
            prompt_pdf = PdfReader(prompt_buffer)
            prompt_page = prompt_pdf.pages[0]
            
            # Scale the prompt overlay
            prompt_page.scale_to(page_width, page_height)
            
            # Merge the prompt overlay with the already modified page
            page.merge_page(prompt_page)
        
        # Add the modified page to the output PDF
        writer.add_page(page)

    # Write the output PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inject invisible text into PDF files")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_pdf", help="Path where the modified PDF will be saved")
    parser.add_argument(
        "text", help="Text to inject (invisible to humans, readable by machines)"
    )
    parser.add_argument(
        "--prompt", 
        help=(
            "Custom tiny visible prompt text to add to the last page "
            "(default: 'PDF enhanced with invisible searchable text')"
        ), 
        default="PDF enhanced with invisible searchable text"
    )
    parser.add_argument(
        "--no-prompt", 
        help="Don't add any visible prompt text", 
        action="store_true"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_pdf):
        print(f"Error: Input file '{args.input_pdf}' not found")
        return 1

    try:
        # Modify inject_invisible_text function to handle prompt options
        prompt_text = None if args.no_prompt else args.prompt
        inject_invisible_text(args.input_pdf, args.output_pdf, args.text, prompt_text)
        print(f"Successfully injected invisible text into '{args.output_pdf}'")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
