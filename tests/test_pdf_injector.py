import os
import tempfile

from main import (
    create_invisible_text_layer,
    create_tiny_prompt_layer,
    inject_invisible_text,
)

# Sample test text
TEST_TEXT = "This is invisible test text"
TEST_PROMPT = "This is a tiny prompt"


def test_create_invisible_text_layer():
    """Test that invisible text layer is created successfully."""
    buffer = create_invisible_text_layer(TEST_TEXT)

    # Check that buffer contains data
    assert buffer.getvalue(), "Buffer should not be empty"

    # Check that buffer contains PDF signature
    assert buffer.getvalue()[:4] == b"%PDF", "Buffer should contain PDF data"


def test_create_tiny_prompt_layer():
    """Test that tiny prompt layer is created successfully."""
    buffer = create_tiny_prompt_layer((595, 842), TEST_PROMPT)

    # Check that buffer contains data
    assert buffer.getvalue(), "Buffer should not be empty"

    # Check that buffer contains PDF signature
    assert buffer.getvalue()[:4] == b"%PDF", "Buffer should contain PDF data"


def test_inject_invisible_text_with_temp_files():
    """Test PDF injection using temporary files."""
    # Create a simple PDF for testing
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as input_pdf:
        # Create a minimal valid PDF (empty page)
        # Break up the long line to avoid linting errors
        pdf_content = (
            b"%PDF-1.7\n"
            b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
            b"3 0 obj<</Type/Page/MediaBox[0 0 595 842]/Parent 2 0 R>>endobj\n"
            b"xref\n0 4\n"
            b"0000000000 65535 f\n"
            b"0000000009 00000 n\n"
            b"0000000052 00000 n\n"
            b"0000000103 00000 n\n"
            b"trailer<</Size 4/Root 1 0 R>>\n"
            b"startxref\n171\n%%EOF"
        )
        input_pdf.write(pdf_content)

    # Output file paths
    output_path = input_pdf.name + ".output.pdf"
    output_path_with_prompt = input_pdf.name + ".prompt.pdf"

    try:
        # Test without prompt (None)
        inject_invisible_text(input_pdf.name, output_path, TEST_TEXT, None)
        
        # Test with prompt
        inject_invisible_text(
            input_pdf.name, output_path_with_prompt, TEST_TEXT, TEST_PROMPT
        )

        # Check that both output files exist and have content
        for path in [output_path, output_path_with_prompt]:
            assert os.path.exists(path), f"Output file {path} should exist"
            assert os.path.getsize(path) > 0, f"Output file {path} should have content"

            # Basic validation that it's still a PDF
            with open(path, "rb") as f:
                content = f.read(4)
                assert content == b"%PDF", f"Output {path} should be a valid PDF"

        # File with prompt should be larger than file without prompt
        assert (
            os.path.getsize(output_path_with_prompt) > os.path.getsize(output_path)
        ), "Prompted file should be larger than non-prompted file"

    finally:
        # Clean up test files
        if os.path.exists(input_pdf.name):
            os.unlink(input_pdf.name)
        for path in [output_path, output_path_with_prompt]:
            if os.path.exists(path):
                os.unlink(path)
