"""
Create a visual preview of the presentation slides
Shows what each slide would look like in the PowerPoint
"""
import json


def create_slide_preview():
    """Generate ASCII art preview of slides"""

    with open('/tmp/presentation_structure.json', 'r') as f:
        content = json.load(f)

    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*20 + "PRESENTATION PREVIEW" + " "*38 + "║")
    print("╚" + "═"*78 + "╝")
    print()

    for i, slide in enumerate(content['slides'], 1):
        # Create slide border
        print("┌" + "─"*78 + "┐")

        # Slide number and title
        print("│" + f" Slide {i}/{len(content['slides'])}".ljust(78) + "│")
        print("│" + "─"*78 + "│")

        # Title (centered and bold effect)
        title = slide['title'].upper()
        padding = (78 - len(title)) // 2
        print("│" + " "*padding + title + " "*(78-padding-len(title)) + "│")

        # Section tag if present
        if slide.get('section'):
            section_tag = f"[{slide['section']}]"
            padding = (78 - len(section_tag)) // 2
            print("│" + " "*padding + section_tag + " "*(78-padding-len(section_tag)) + "│")

        print("│" + " "*78 + "│")

        # Content area
        content_lines = slide['content']
        max_content_lines = 6

        # If there's a diagram, show it on the right side
        if slide.get('diagram_type') and slide['diagram_type'] != 'none':
            diagram_type = slide['diagram_type']
            diagram_width = 35

            # Show content on left, diagram placeholder on right
            for j in range(max_content_lines):
                left_side = ""
                if j < len(content_lines):
                    bullet = content_lines[j]
                    if len(bullet) > 38:
                        bullet = bullet[:35] + "..."
                    left_side = f"  • {bullet}".ljust(42)
                else:
                    left_side = " " * 42

                # Diagram placeholder
                if j == 0:
                    right_side = "┌─ DIAGRAM ─────────────────┐"
                elif j == 1:
                    if diagram_type == 'medallion':
                        right_side = "│  [Bronze → Silver → Gold] │"
                    else:
                        right_side = f"│  [{diagram_type.title()}]".ljust(28) + " │"
                elif j == max_content_lines - 1:
                    right_side = "└───────────────────────────┘"
                else:
                    right_side = "│                           │"

                print("│" + left_side + right_side.ljust(36) + "│")
        else:
            # Full width content
            for j in range(min(len(content_lines), max_content_lines)):
                bullet = content_lines[j]
                if len(bullet) > 72:
                    bullet = bullet[:69] + "..."
                line = f"  • {bullet}".ljust(78)
                print("│" + line + "│")

            # Fill empty lines
            for j in range(len(content_lines), max_content_lines):
                print("│" + " "*78 + "│")

        # Bottom border
        print("└" + "─"*78 + "┘")
        print()

    print("╔" + "═"*78 + "╗")
    print("║" + " "*15 + "DATABRICKS BRANDING COLORS APPLIED" + " "*29 + "║")
    print("║" + " "*10 + "Red Accent (#FF3621) • Dark Navy (#1B3139)" + " "*21 + "║")
    print("║" + " "*10 + "Bronze/Silver/Gold for Medallion Diagrams" + " "*21 + "║")
    print("╚" + "═"*78 + "╝")
    print()


if __name__ == "__main__":
    create_slide_preview()
