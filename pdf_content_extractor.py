"""
PDF Content Extractor
Extracts content from PDF files to generate PowerPoint presentations
"""
import pdfplumber
import pypdf
from typing import Dict, List, Any
import re


class PDFContentExtractor:
    """Extract content from PDF files for presentation generation"""

    def __init__(self):
        """Initialize the content extractor"""
        pass

    def extract_content(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract content from a PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing extracted content structured for presentation
        """
        content = {
            'title': '',
            'pages': [],
            'text_blocks': [],
            'headings': [],
            'bullet_points': [],
            'images': []
        }

        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Extract title from first page
                if len(pdf.pages) > 0:
                    first_page = pdf.pages[0]
                    text = first_page.extract_text()

                    if text:
                        lines = text.split('\n')
                        # First non-empty line is often the title
                        for line in lines:
                            if line.strip():
                                content['title'] = line.strip()
                                break

                # Extract content from all pages
                for page_num, page in enumerate(pdf.pages):
                    page_content = self._extract_page_content(page, page_num)
                    content['pages'].append(page_content)

            # Structure content for presentation
            structured = self._structure_for_presentation(content)
            return structured

        except Exception as e:
            print(f"Error extracting PDF content: {e}")
            return {
                'title': 'Extracted from PDF',
                'slides': []
            }

    def _extract_page_content(self, page, page_num: int) -> Dict[str, Any]:
        """Extract content from a single PDF page"""
        page_data = {
            'page_number': page_num + 1,
            'text': '',
            'headings': [],
            'paragraphs': [],
            'bullets': [],
            'images': []
        }

        # Extract text
        text = page.extract_text()
        if text:
            page_data['text'] = text

            # Try to identify headings (larger font size or bold)
            chars = page.chars
            if chars:
                # Analyze font sizes
                font_sizes = [char.get('size', 0) for char in chars if char.get('size')]
                if font_sizes:
                    avg_size = sum(font_sizes) / len(font_sizes)
                    max_size = max(font_sizes)

                    # Lines with larger than average font are likely headings
                    current_line = []
                    current_size = 0

                    for char in chars:
                        size = char.get('size', 0)
                        text_char = char.get('text', '')

                        if text_char == '\n':
                            if current_line and current_size > avg_size * 1.2:
                                heading = ''.join(current_line).strip()
                                if heading:
                                    page_data['headings'].append(heading)
                            current_line = []
                            current_size = 0
                        else:
                            current_line.append(text_char)
                            current_size = max(current_size, size)

            # Extract bullet points (lines starting with common bullet markers)
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # Check for bullet markers
                if line and (line.startswith('•') or line.startswith('-') or
                           line.startswith('*') or re.match(r'^\d+\.', line)):
                    # Remove bullet marker
                    clean_line = re.sub(r'^[•\-*]\s*', '', line)
                    clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
                    page_data['bullets'].append(clean_line.strip())
                elif line and len(line) > 20:  # Regular paragraph
                    page_data['paragraphs'].append(line)

        # Extract images
        if hasattr(page, 'images') and page.images:
            page_data['images'] = page.images

        return page_data

    def _structure_for_presentation(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure extracted content into presentation format

        Args:
            content: Raw extracted content

        Returns:
            Structured presentation content
        """
        slides = []

        # Title slide
        title = content.get('title', 'Presentation from PDF')
        slides.append({
            'title': title,
            'content': [
                'Generated from PDF document',
                'Review and edit as needed'
            ],
            'section': None,
            'diagram_type': 'none',
            'diagram_description': None
        })

        # Process pages into slides
        for page in content.get('pages', []):
            # Skip first page if it's just title
            if page['page_number'] == 1 and not page.get('bullets') and not page.get('paragraphs'):
                continue

            # Use headings as slide titles
            headings = page.get('headings', [])
            bullets = page.get('bullets', [])
            paragraphs = page.get('paragraphs', [])

            # If we have headings and bullets, create slides
            if headings and bullets:
                for heading in headings:
                    slides.append({
                        'title': heading,
                        'content': bullets[:5],  # Limit to 5 bullets per slide
                        'section': None,
                        'diagram_type': 'none',
                        'diagram_description': None
                    })
                    bullets = bullets[5:]  # Use remaining bullets for next slide
            elif headings and paragraphs:
                # Convert paragraphs to bullet points
                for heading in headings:
                    slide_content = paragraphs[:3]  # Up to 3 paragraphs
                    slides.append({
                        'title': heading,
                        'content': slide_content,
                        'section': None,
                        'diagram_type': 'none',
                        'diagram_description': None
                    })
                    paragraphs = paragraphs[3:]
            elif bullets:
                # Create slide from bullets without specific heading
                slides.append({
                    'title': f'Page {page["page_number"]}',
                    'content': bullets[:6],
                    'section': None,
                    'diagram_type': 'none',
                    'diagram_description': None
                })

        return {
            'title': title,
            'slides': slides
        }

    def merge_with_prompt_modifications(
        self,
        extracted_content: Dict[str, Any],
        modification_prompt: str
    ) -> str:
        """
        Create a prompt that combines extracted PDF content with modification instructions

        Args:
            extracted_content: Content extracted from PDF
            modification_prompt: User's instructions for modifications

        Returns:
            Combined prompt for Claude AI
        """
        # Summarize extracted content
        num_slides = len(extracted_content.get('slides', []))
        title = extracted_content.get('title', 'Document')

        combined_prompt = f"""I have extracted content from a PDF document titled "{title}"
with {num_slides} slides.

Original content structure:
"""

        # Add sample of original content
        for i, slide in enumerate(extracted_content.get('slides', [])[:3], 1):
            combined_prompt += f"\nSlide {i}: {slide.get('title', 'Untitled')}\n"
            for bullet in slide.get('content', [])[:3]:
                combined_prompt += f"  • {bullet}\n"

        combined_prompt += f"\n\nModification Instructions:\n{modification_prompt}\n"

        combined_prompt += "\n\nPlease create an improved presentation incorporating these modifications."

        return combined_prompt
