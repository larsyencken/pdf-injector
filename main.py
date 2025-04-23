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
        c.drawString(50, y_position, line)
        y_position -= 15

    c.save()
    buffer.seek(0)
    return buffer


def inject_invisible_text(input_pdf_path: str, output_pdf_path: str, text: str) -> None:
    """Inject invisible text into an existing PDF."""
    # Read the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Process each page
    for i, page in enumerate(reader.pages):
        # Create invisible text overlay for current page
        overlay_buffer = create_invisible_text_layer(text)
        overlay_pdf = PdfReader(overlay_buffer)
        overlay_page = overlay_pdf.pages[0]

        # Get the original page dimensions
        page_width = page.mediabox.width
        page_height = page.mediabox.height

        # Scale the overlay to match the original page size
        overlay_page.scale_to(page_width, page_height)

        # Merge the original page with the overlay
        page.merge_page(overlay_page)

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

    args = parser.parse_args()

    if not os.path.exists(args.input_pdf):
        print(f"Error: Input file '{args.input_pdf}' not found")
        return 1

    try:
        inject_invisible_text(args.input_pdf, args.output_pdf, args.text)
        print(f"Successfully injected invisible text into '{args.output_pdf}'")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
