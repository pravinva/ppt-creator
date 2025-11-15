"""
Additional callbacks for PDF handling
These handle branding PDF and content PDF uploads
"""
from dash import html
import base64
import tempfile
import os
from pdf_branding_analyzer import BrandingExtractor
from pdf_content_extractor import PDFContentExtractor


def parse_pdf_contents(contents, filename):
    """Parse uploaded PDF contents"""
    try:
        # Decode the base64 encoded content
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(decoded)
            tmp_path = tmp_file.name

        return tmp_path, filename
    except Exception as e:
        return None, str(e)


def handle_branding_pdf_upload(contents, filename):
    """Handle branding PDF upload and extract branding"""
    if contents is None:
        return None, None

    tmp_path, result = parse_pdf_contents(contents, filename)

    if tmp_path is None:
        status = html.Div([
            html.Div(f"Error: {result}", className="status-indicator status-error")
        ])
        return status, None

    try:
        # Extract branding
        extractor = BrandingExtractor()
        branding = extractor.analyze_pdf(tmp_path)

        # Clean up temp file
        os.unlink(tmp_path)

        # Create status message
        summary = extractor.get_branding_summary(branding)
        status = html.Div([
            html.Div([
                html.I(className="bi bi-check-circle-fill me-2"),
                f"Branding extracted from {filename}"
            ], className="status-indicator status-success"),
            html.Details([
                html.Summary("View branding details", style={'cursor': 'pointer', 'marginTop': '5px'}),
                html.Pre(summary, style={'fontSize': '12px', 'marginTop': '10px'})
            ])
        ])

        return status, branding

    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

        status = html.Div([
            html.Div(f"Error extracting branding: {str(e)}", className="status-indicator status-error")
        ])
        return status, None


def handle_content_pdf_upload(contents, filename):
    """Handle content PDF upload and extract content"""
    if contents is None:
        return None, None

    tmp_path, result = parse_pdf_contents(contents, filename)

    if tmp_path is None:
        status = html.Div([
            html.Div(f"Error: {result}", className="status-indicator status-error")
        ])
        return status, None

    try:
        # Extract content
        extractor = PDFContentExtractor()
        content = extractor.extract_content(tmp_path)

        # Clean up temp file
        os.unlink(tmp_path)

        # Create status message
        num_slides = len(content.get('slides', []))
        status = html.Div([
            html.Div([
                html.I(className="bi bi-check-circle-fill me-2"),
                f"Content extracted from {filename}"
            ], className="status-indicator status-success"),
            html.P(f"Found {num_slides} potential slides. Use the prompt field below to modify the content.",
                  className="text-muted mt-2", style={'fontSize': '13px'})
        ])

        return status, content

    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

        status = html.Div([
            html.Div(f"Error extracting content: {str(e)}", className="status-indicator status-error")
        ])
        return status, None
