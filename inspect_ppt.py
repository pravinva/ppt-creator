"""
PowerPoint Slide Inspector
Shows detailed information about the generated PowerPoint
"""
from pptx import Presentation
from pptx.util import Pt
import json


def inspect_powerpoint(pptx_path):
    """Inspect and display PowerPoint details"""

    prs = Presentation(pptx_path)

    print("="*80)
    print("POWERPOINT FILE INSPECTION")
    print("="*80)
    print()

    # Basic info
    print(f"File: {pptx_path}")
    print(f"Slide Dimensions: {prs.slide_width.inches:.1f}\" × {prs.slide_height.inches:.1f}\"")
    print(f"Total Slides: {len(prs.slides)}")
    print()

    print("-"*80)
    print()

    # Inspect each slide
    for slide_num, slide in enumerate(prs.slides, 1):
        print(f"SLIDE {slide_num}")
        print("-" * 40)

        # Count elements
        shapes_count = len(slide.shapes)
        text_boxes = 0
        images = 0
        rectangles = 0

        texts = []

        for shape in slide.shapes:
            if shape.has_text_frame:
                text_boxes += 1
                # Extract text
                for paragraph in shape.text_frame.paragraphs:
                    text = paragraph.text.strip()
                    if text:
                        texts.append(text)

            if shape.shape_type == 13:  # Picture
                images += 1
            elif shape.shape_type == 1:  # Rectangle
                rectangles += 1

        print(f"  Elements: {shapes_count} total")
        print(f"  - Text boxes: {text_boxes}")
        print(f"  - Images/Diagrams: {images}")
        print(f"  - Rectangles: {rectangles}")
        print()

        # Show text content
        if texts:
            print("  Text Content:")
            for i, text in enumerate(texts[:8], 1):  # First 8 text elements
                preview = text[:70] + "..." if len(text) > 70 else text
                print(f"    {i}. {preview}")

        print()

    print("="*80)
    print("BRANDING ANALYSIS")
    print("="*80)
    print()

    # Analyze colors used
    colors_found = set()
    fonts_found = set()

    for slide in prs.slides:
        for shape in slide.shapes:
            # Check fill colors
            if shape.fill.type:
                try:
                    if hasattr(shape.fill, 'fore_color') and hasattr(shape.fill.fore_color, 'rgb'):
                        rgb = shape.fill.fore_color.rgb
                        colors_found.add(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
                except:
                    pass

            # Check fonts
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.name:
                            fonts_found.add(run.font.name)

    print("Colors Used:")
    for color in sorted(colors_found):
        # Identify Databricks colors
        color_name = ""
        if color.upper() == "#FF3621":
            color_name = " (Databricks Red)"
        elif color.upper() == "#1B3139":
            color_name = " (Databricks Dark Navy)"
        elif color.upper() == "#FFFFFF":
            color_name = " (White)"

        print(f"  • {color.upper()}{color_name}")

    print()
    print("Fonts Used:")
    for font in sorted(fonts_found):
        print(f"  • {font}")

    print()
    print("="*80)


if __name__ == "__main__":
    inspect_powerpoint("/tmp/genie_mcp_zerobus_demo.pptx")
