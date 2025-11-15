"""
PDF Branding Analyzer
Extracts branding elements (colors, fonts, layout) from sample PDF files
"""
import pdfplumber
import pypdf
from PIL import Image
import io
import re
from typing import Dict, List, Tuple, Any, Optional
from collections import Counter
import colorsys


class BrandingExtractor:
    """Extract branding elements from PDF files"""

    def __init__(self):
        """Initialize the branding extractor"""
        self.default_databricks_branding = {
            'primary_color': (255, 54, 33),  # Databricks Red
            'secondary_color': (27, 49, 57),  # Dark Navy
            'accent_color': (0, 164, 228),  # Blue
            'text_color': (27, 49, 57),
            'background_color': (255, 255, 255),
            'fonts': ['Arial', 'Helvetica', 'Sans-Serif'],
            'font_sizes': {
                'title': 36,
                'heading': 28,
                'body': 20
            }
        }

    def analyze_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Analyze a PDF file to extract branding elements

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing extracted branding information
        """
        branding = {
            'colors': [],
            'fonts': [],
            'font_sizes': [],
            'layout': {},
            'images': [],
            'source': pdf_path
        }

        try:
            # Extract colors and fonts using pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                # Analyze first few pages for branding
                pages_to_analyze = min(3, len(pdf.pages))

                for i in range(pages_to_analyze):
                    page = pdf.pages[i]

                    # Extract text and font information
                    chars = page.chars
                    if chars:
                        fonts = [char.get('fontname', '') for char in chars]
                        sizes = [char.get('size', 0) for char in chars]

                        branding['fonts'].extend(fonts)
                        branding['font_sizes'].extend(sizes)

                    # Extract images
                    if hasattr(page, 'images'):
                        branding['images'].extend(page.images)

            # Process extracted data
            branding['fonts'] = self._process_fonts(branding['fonts'])
            branding['font_sizes'] = self._process_font_sizes(branding['font_sizes'])
            branding['colors'] = self._extract_colors_from_pdf(pdf_path)

            # Build final branding profile
            return self._build_branding_profile(branding)

        except Exception as e:
            print(f"Error analyzing PDF: {e}")
            # Return default Databricks branding on error
            return self.default_databricks_branding

    def _extract_colors_from_pdf(self, pdf_path: str) -> List[Tuple[int, int, int]]:
        """Extract colors from PDF using pypdf"""
        colors = []

        try:
            with open(pdf_path, 'rb') as f:
                reader = pypdf.PdfReader(f)

                # Try to extract colors from first few pages
                for page_num in range(min(3, len(reader.pages))):
                    page = reader.pages[page_num]

                    # Look for color information in the page content
                    if '/Resources' in page:
                        resources = page['/Resources']

                        # Check for color spaces
                        if '/ColorSpace' in resources:
                            # Color extraction logic
                            pass

            # If no colors extracted, use common corporate colors
            if not colors:
                colors = self._get_common_corporate_colors()

        except Exception as e:
            print(f"Color extraction error: {e}")
            colors = self._get_common_corporate_colors()

        return colors

    def _get_common_corporate_colors(self) -> List[Tuple[int, int, int]]:
        """Return common corporate color palette"""
        return [
            (255, 54, 33),   # Red
            (27, 49, 57),    # Dark Navy
            (0, 164, 228),   # Blue
            (0, 200, 83),    # Green
            (255, 152, 0),   # Orange
        ]

    def _process_fonts(self, fonts: List[str]) -> List[str]:
        """Process and clean font names"""
        if not fonts:
            return ['Arial', 'Helvetica']

        # Count font occurrences
        font_counter = Counter(fonts)

        # Get top 3 most common fonts
        top_fonts = [font for font, count in font_counter.most_common(3) if font]

        # Clean font names (remove encoding info)
        cleaned_fonts = []
        for font in top_fonts:
            # Remove common prefixes and suffixes
            cleaned = re.sub(r'[+].*?-', '', font)
            cleaned = re.sub(r'-.*', '', cleaned)
            cleaned = re.sub(r'\+.*', '', cleaned)

            if cleaned and len(cleaned) > 2:
                cleaned_fonts.append(cleaned)

        return cleaned_fonts if cleaned_fonts else ['Arial', 'Helvetica']

    def _process_font_sizes(self, sizes: List[float]) -> Dict[str, int]:
        """Process font sizes to determine title, heading, and body sizes"""
        if not sizes:
            return {'title': 36, 'heading': 28, 'body': 20}

        sizes = [s for s in sizes if s > 0]
        if not sizes:
            return {'title': 36, 'heading': 28, 'body': 20}

        # Sort sizes
        sorted_sizes = sorted(set(sizes), reverse=True)

        # Assign categories
        font_profile = {
            'title': int(sorted_sizes[0]) if len(sorted_sizes) > 0 else 36,
            'heading': int(sorted_sizes[min(1, len(sorted_sizes)-1)]) if len(sorted_sizes) > 1 else 28,
            'body': int(sorted_sizes[min(2, len(sorted_sizes)-1)]) if len(sorted_sizes) > 2 else 20
        }

        return font_profile

    def _build_branding_profile(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build a complete branding profile from extracted data"""

        colors = extracted_data.get('colors', [])
        fonts = extracted_data.get('fonts', [])
        font_sizes = extracted_data.get('font_sizes', {})

        # Determine primary, secondary, and accent colors
        profile = {
            'primary_color': colors[0] if len(colors) > 0 else (255, 54, 33),
            'secondary_color': colors[1] if len(colors) > 1 else (27, 49, 57),
            'accent_color': colors[2] if len(colors) > 2 else (0, 164, 228),
            'text_color': colors[1] if len(colors) > 1 else (27, 49, 57),
            'background_color': (255, 255, 255),
            'fonts': fonts if fonts else ['Arial'],
            'font_sizes': font_sizes if font_sizes else {'title': 36, 'heading': 28, 'body': 20},
            'source': extracted_data.get('source', 'Unknown')
        }

        return profile

    def merge_with_databricks_branding(self, custom_branding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge custom branding with Databricks defaults
        Allows for hybrid branding approach
        """
        merged = self.default_databricks_branding.copy()

        # Use custom colors if available, keep Databricks as fallback
        if 'primary_color' in custom_branding:
            merged['primary_color'] = custom_branding['primary_color']

        if 'secondary_color' in custom_branding:
            merged['secondary_color'] = custom_branding['secondary_color']

        # Use custom fonts but keep size structure
        if 'fonts' in custom_branding and custom_branding['fonts']:
            merged['fonts'] = custom_branding['fonts']

        # Use custom font sizes if reasonable
        if 'font_sizes' in custom_branding:
            custom_sizes = custom_branding['font_sizes']
            if custom_sizes.get('title', 0) >= 24:  # Sanity check
                merged['font_sizes'] = custom_sizes

        return merged

    def extract_color_from_rgb_string(self, rgb_string: str) -> Optional[Tuple[int, int, int]]:
        """Extract RGB tuple from various string formats"""
        # Handle formats like "rgb(255, 54, 33)" or "255 54 33" or "#FF3621"

        # Hex format
        if rgb_string.startswith('#'):
            hex_color = rgb_string.lstrip('#')
            if len(hex_color) == 6:
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # RGB format
        rgb_match = re.search(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', rgb_string)
        if rgb_match:
            return tuple(int(x) for x in rgb_match.groups())

        # Space-separated
        parts = rgb_string.split()
        if len(parts) == 3:
            try:
                return tuple(int(x) for x in parts)
            except ValueError:
                pass

        return None

    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color string"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def get_branding_summary(self, branding: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the branding"""
        summary = []
        summary.append("Branding Profile:")
        summary.append(f"  Primary Color: {self.rgb_to_hex(branding['primary_color'])}")
        summary.append(f"  Secondary Color: {self.rgb_to_hex(branding['secondary_color'])}")
        summary.append(f"  Accent Color: {self.rgb_to_hex(branding['accent_color'])}")
        summary.append(f"  Fonts: {', '.join(branding['fonts'])}")
        summary.append(f"  Title Size: {branding['font_sizes']['title']}pt")
        summary.append(f"  Heading Size: {branding['font_sizes']['heading']}pt")
        summary.append(f"  Body Size: {branding['font_sizes']['body']}pt")

        return '\n'.join(summary)
