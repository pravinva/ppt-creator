"""
PowerPoint Modifier
Read and modify existing PowerPoint presentations
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from typing import Dict, List, Any, Optional
import io
import copy


class PPTXModifier:
    """Modify existing PowerPoint presentations"""

    def __init__(self, pptx_path: Optional[str] = None):
        """
        Initialize with optional existing presentation

        Args:
            pptx_path: Path to existing PPTX file (optional)
        """
        if pptx_path:
            self.prs = Presentation(pptx_path)
            self.is_new = False
        else:
            self.prs = Presentation()
            self.is_new = True

    def extract_content(self) -> Dict[str, Any]:
        """
        Extract content from existing PowerPoint

        Returns:
            Dictionary with title and slides content
        """
        slides_content = []

        for slide_num, slide in enumerate(self.prs.slides, 1):
            slide_data = {
                'slide_number': slide_num,
                'title': '',
                'content': [],
                'has_images': False,
                'layout_name': slide.slide_layout.name if hasattr(slide, 'slide_layout') else 'Unknown'
            }

            # Extract text from all shapes
            for shape in slide.shapes:
                if shape.has_text_frame:
                    text = shape.text.strip()
                    if text:
                        # First substantial text is usually the title
                        if not slide_data['title'] and len(text) < 100:
                            slide_data['title'] = text
                        else:
                            # Extract paragraphs/bullets
                            for paragraph in shape.text_frame.paragraphs:
                                para_text = paragraph.text.strip()
                                if para_text and para_text != slide_data['title']:
                                    slide_data['content'].append(para_text)

                # Check for images
                if shape.shape_type == 13:  # Picture
                    slide_data['has_images'] = True

            slides_content.append(slide_data)

        # Determine title from first slide
        title = "Extracted PowerPoint"
        if slides_content and slides_content[0]['title']:
            title = slides_content[0]['title']

        return {
            'title': title,
            'total_slides': len(slides_content),
            'slides': slides_content,
            'slide_dimensions': {
                'width': self.prs.slide_width.inches,
                'height': self.prs.slide_height.inches
            }
        }

    def modify_slide_text(self, slide_index: int, replacements: Dict[str, str]):
        """
        Modify text in a specific slide

        Args:
            slide_index: 0-based slide index
            replacements: Dictionary of {old_text: new_text}
        """
        if slide_index >= len(self.prs.slides):
            raise ValueError(f"Slide index {slide_index} out of range")

        slide = self.prs.slides[slide_index]

        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        for old_text, new_text in replacements.items():
                            if old_text in run.text:
                                run.text = run.text.replace(old_text, new_text)

    def apply_branding(self, branding: Dict[str, Any]):
        """
        Apply custom branding to all slides

        Args:
            branding: Dictionary with primary_color, secondary_color, fonts, etc.
        """
        primary_rgb = branding.get('primary_color', (255, 54, 33))
        text_rgb = branding.get('text_color', (27, 49, 57))
        fonts = branding.get('fonts', ['Arial'])

        for slide in self.prs.slides:
            for shape in slide.shapes:
                # Update text colors and fonts
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            run.font.color.rgb = RGBColor(*text_rgb)
                            if fonts:
                                run.font.name = fonts[0]

                # Update shape fills (accent bars, backgrounds)
                if hasattr(shape, 'fill') and shape.fill.type:
                    try:
                        # Only change colored fills, not white backgrounds
                        if hasattr(shape.fill, 'fore_color'):
                            current_rgb = shape.fill.fore_color.rgb
                            # If it's a colored element (not white), apply primary color
                            if current_rgb != (255, 255, 255):
                                shape.fill.solid()
                                shape.fill.fore_color.rgb = RGBColor(*primary_rgb)
                    except:
                        pass

    def add_slide_at_position(self, position: int, layout_index: int = 6):
        """
        Add a new slide at specific position

        Args:
            position: Position to insert (0-based)
            layout_index: Slide layout to use (default 6 = blank)
        """
        slide_layout = self.prs.slide_layouts[layout_index]
        new_slide = self.prs.slides.add_slide(slide_layout)

        # Move to desired position
        xml_slides = self.prs.slides._sldIdLst
        slides_list = list(xml_slides)
        xml_slides.remove(slides_list[-1])
        xml_slides.insert(position, slides_list[-1])

        return new_slide

    def delete_slide(self, slide_index: int):
        """
        Delete a slide

        Args:
            slide_index: 0-based slide index
        """
        if slide_index >= len(self.prs.slides):
            raise ValueError(f"Slide index {slide_index} out of range")

        rId = self.prs.slides._sldIdLst[slide_index].rId
        self.prs.part.drop_rel(rId)
        del self.prs.slides._sldIdLst[slide_index]

    def reorder_slides(self, new_order: List[int]):
        """
        Reorder slides based on list of indices

        Args:
            new_order: List of slide indices in desired order
                      e.g., [0, 2, 1, 3] moves slide 2 before slide 1
        """
        if len(new_order) != len(self.prs.slides):
            raise ValueError("new_order must contain all slide indices")

        xml_slides = self.prs.slides._sldIdLst
        slides_list = list(xml_slides)

        # Clear current order
        for slide in slides_list:
            xml_slides.remove(slide)

        # Add in new order
        for idx in new_order:
            xml_slides.append(slides_list[idx])

    def duplicate_slide(self, slide_index: int) -> int:
        """
        Duplicate a slide

        Args:
            slide_index: 0-based index of slide to duplicate

        Returns:
            Index of new slide
        """
        if slide_index >= len(self.prs.slides):
            raise ValueError(f"Slide index {slide_index} out of range")

        source_slide = self.prs.slides[slide_index]

        # Use same layout
        blank_layout = self.prs.slide_layouts[6]
        new_slide = self.prs.slides.add_slide(blank_layout)

        # Copy all shapes from source
        for shape in source_slide.shapes:
            el = shape.element
            newel = copy.deepcopy(el)
            new_slide.shapes._spTree.insert_element_before(newel, 'p:extLst')

        return len(self.prs.slides) - 1

    def merge_presentations(self, other_pptx_path: str):
        """
        Merge another presentation into this one

        Args:
            other_pptx_path: Path to PowerPoint file to merge
        """
        other_prs = Presentation(other_pptx_path)

        for slide in other_prs.slides:
            # Add slide with same layout
            try:
                layout = self.prs.slide_layouts[slide.slide_layout.name]
            except:
                layout = self.prs.slide_layouts[6]  # Blank if layout not found

            new_slide = self.prs.slides.add_slide(layout)

            # Copy shapes
            for shape in slide.shapes:
                el = shape.element
                newel = copy.deepcopy(el)
                new_slide.shapes._spTree.insert_element_before(newel, 'p:extLst')

    def add_logo_to_all_slides(self, logo_path: str, position: str = 'top-right',
                               size: float = 0.8, skip_title_slide: bool = False):
        """
        Add logo to all slides

        Args:
            logo_path: Path to logo image file
            position: 'top-right', 'top-left', 'bottom-right', 'bottom-left'
            size: Logo size in inches
            skip_title_slide: Skip first slide if True
        """
        positions = {
            'top-right': (self.prs.slide_width - Inches(size + 0.3), Inches(0.3)),
            'top-left': (Inches(0.3), Inches(0.3)),
            'bottom-right': (self.prs.slide_width - Inches(size + 0.3),
                           self.prs.slide_height - Inches(size + 0.3)),
            'bottom-left': (Inches(0.3), self.prs.slide_height - Inches(size + 0.3))
        }

        left, top = positions.get(position, positions['top-right'])

        start_idx = 1 if skip_title_slide else 0

        for slide in self.prs.slides[start_idx:]:
            slide.shapes.add_picture(logo_path, left, top, height=Inches(size))

    def save(self, output_path: str):
        """Save modified presentation"""
        self.prs.save(output_path)

    def get_summary(self) -> str:
        """Get a summary of the presentation"""
        summary = []
        summary.append(f"PowerPoint Presentation Summary")
        summary.append(f"=" * 50)
        summary.append(f"Total Slides: {len(self.prs.slides)}")
        summary.append(f"Dimensions: {self.prs.slide_width.inches:.1f}\" x {self.prs.slide_height.inches:.1f}\"")
        summary.append(f"Layouts Available: {len(self.prs.slide_layouts)}")
        summary.append("")
        summary.append("Slides:")
        for i, slide in enumerate(self.prs.slides, 1):
            title = "Untitled"
            for shape in slide.shapes:
                if shape.has_text_frame and shape.text.strip():
                    title = shape.text.strip()[:50]
                    break
            summary.append(f"  {i}. {title}")

        return "\n".join(summary)


# Convenience function for quick modifications
def modify_existing_pptx(
    input_path: str,
    output_path: str,
    text_replacements: Optional[Dict[str, str]] = None,
    branding: Optional[Dict[str, Any]] = None,
    logo_path: Optional[str] = None
) -> str:
    """
    Quick modification of existing PowerPoint

    Args:
        input_path: Input PPTX file
        output_path: Output PPTX file
        text_replacements: Dict of text to replace across all slides
        branding: Branding dictionary to apply
        logo_path: Optional logo to add

    Returns:
        Summary of modifications
    """
    modifier = PPTXModifier(input_path)

    modifications = []

    # Apply text replacements
    if text_replacements:
        for i in range(len(modifier.prs.slides)):
            modifier.modify_slide_text(i, text_replacements)
        modifications.append(f"Applied {len(text_replacements)} text replacements")

    # Apply branding
    if branding:
        modifier.apply_branding(branding)
        modifications.append("Applied custom branding")

    # Add logo
    if logo_path:
        modifier.add_logo_to_all_slides(logo_path)
        modifications.append("Added logo to all slides")

    # Save
    modifier.save(output_path)

    summary = f"Modified presentation saved to {output_path}\n"
    summary += f"Modifications: {', '.join(modifications)}"

    return summary
