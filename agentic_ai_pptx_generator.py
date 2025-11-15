"""
Generic Agentic AI PowerPoint Generator
Works for ANY company based on prompts

Generates professional presentations from architecture diagrams
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from PIL import Image
import os


class AgenticAIPPTXGenerator:
    """
    Generic PPTX generator for Agentic AI presentations
    Works for any company
    """

    # Modern Databricks 2025 colors
    NAVY = RGBColor(27, 49, 57)
    ORANGE = RGBColor(255, 54, 33)
    LIGHT_BLUE = RGBColor(97, 135, 148)
    WHITE = RGBColor(255, 255, 255)
    LIGHT_GRAY = RGBColor(239, 239, 239)

    def __init__(self):
        """Initialize presentation"""
        self.prs = Presentation()
        self.prs.slide_width = Inches(10)
        self.prs.slide_height = Inches(7.5)

    def add_title_slide(self, company_name: str, subtitle: str = "Agentic AI Journey"):
        """Add title slide"""
        slide_layout = self.prs.slide_layouts[6]  # Blank
        slide = self.prs.slides.add_slide(slide_layout)

        # Background
        background = slide.shapes.add_shape(
            1, 0, 0, self.prs.slide_width, self.prs.slide_height
        )
        background.fill.solid()
        background.fill.fore_color.rgb = self.WHITE
        background.line.color.rgb = self.WHITE

        # Orange accent bar
        accent = slide.shapes.add_shape(
            1, 0, 0, self.prs.slide_width, Inches(0.4)
        )
        accent.fill.solid()
        accent.fill.fore_color.rgb = self.ORANGE
        accent.line.color.rgb = self.ORANGE

        # Company name
        title_box = slide.shapes.add_textbox(
            Inches(1), Inches(2.5), Inches(8), Inches(2)
        )
        title_frame = title_box.text_frame
        title_frame.text = company_name

        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(60)
        title_para.font.bold = True
        title_para.font.color.rgb = self.NAVY
        title_para.alignment = PP_ALIGN.CENTER

        # Subtitle
        subtitle_box = slide.shapes.add_textbox(
            Inches(1), Inches(4), Inches(8), Inches(1.5)
        )
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.text = subtitle

        for para in subtitle_frame.paragraphs:
            para.font.size = Pt(32)
            para.font.color.rgb = self.LIGHT_BLUE
            para.alignment = PP_ALIGN.CENTER

        # Footer
        footer_box = slide.shapes.add_textbox(
            Inches(1), Inches(6.5), Inches(8), Inches(0.5)
        )
        footer_frame = footer_box.text_frame
        footer_frame.text = "Powered by Databricks Lakehouse Platform"

        footer_para = footer_frame.paragraphs[0]
        footer_para.font.size = Pt(14)
        footer_para.font.color.rgb = self.NAVY
        footer_para.alignment = PP_ALIGN.CENTER

    def add_diagram_slide(self, title: str, image_path: str, subtitle: str = ""):
        """Add slide with diagram"""
        if not os.path.exists(image_path):
            print(f"⚠️  Warning: Image not found: {image_path}")
            return

        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)

        # Background
        background = slide.shapes.add_shape(
            1, 0, 0, self.prs.slide_width, self.prs.slide_height
        )
        background.fill.solid()
        background.fill.fore_color.rgb = self.WHITE
        background.line.color.rgb = self.WHITE

        # Title
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.3), Inches(9), Inches(0.6)
        )
        title_frame = title_box.text_frame
        title_frame.text = title

        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(32)
        title_para.font.bold = True
        title_para.font.color.rgb = self.NAVY

        # Subtitle
        top_offset = Inches(1.1)
        if subtitle:
            subtitle_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(0.85), Inches(9), Inches(0.4)
            )
            subtitle_frame = subtitle_box.text_frame
            subtitle_frame.text = subtitle

            subtitle_para = subtitle_frame.paragraphs[0]
            subtitle_para.font.size = Pt(18)
            subtitle_para.font.italic = True
            subtitle_para.font.color.rgb = self.LIGHT_BLUE
            top_offset = Inches(1.4)

        # Add image
        img = Image.open(image_path)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        max_width = Inches(9)
        max_height = Inches(7.5) - top_offset - Inches(0.3)

        if aspect_ratio > (max_width / max_height):
            width = max_width
            height = width / aspect_ratio
        else:
            height = max_height
            width = height * aspect_ratio

        left = (self.prs.slide_width - width) / 2
        slide.shapes.add_picture(image_path, left, top_offset, width=width)

    def add_content_slide(self, title: str, content: list):
        """Add text content slide"""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)

        # Background
        background = slide.shapes.add_shape(
            1, 0, 0, self.prs.slide_width, self.prs.slide_height
        )
        background.fill.solid()
        background.fill.fore_color.rgb = self.WHITE
        background.line.color.rgb = self.WHITE

        # Title
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.4), Inches(9), Inches(0.7)
        )
        title_frame = title_box.text_frame
        title_frame.text = title

        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(36)
        title_para.font.bold = True
        title_para.font.color.rgb = self.NAVY

        # Content
        content_box = slide.shapes.add_textbox(
            Inches(1), Inches(1.5), Inches(8), Inches(5.5)
        )
        content_frame = content_box.text_frame

        for item in content:
            p = content_frame.add_paragraph()
            p.text = item
            p.font.size = Pt(20)
            p.font.color.rgb = self.NAVY
            p.space_before = Pt(8)

            if item.startswith('•'):
                p.level = 0
            elif item.startswith(('  -', '    •')):
                p.level = 1
                p.font.size = Pt(18)

    def generate_presentation(
        self,
        company_name: str,
        config: dict,
        output_file: str = "Agentic_AI_Presentation.pptx"
    ):
        """
        Generate complete presentation

        Args:
            company_name: Name of company
            config: Configuration dict with slides
            output_file: Output PPTX filename

        Example config:
        {
            "subtitle": "Transformation Roadmap 2025-2026",
            "slides": [
                {
                    "type": "diagram",
                    "title": "Journey Overview",
                    "image": "journey.png",
                    "subtitle": "4-phase transformation"
                },
                {
                    "type": "content",
                    "title": "Benefits",
                    "content": ["• 50% faster", "• 40% cost reduction"]
                }
            ]
        }
        """
        print(f"\n📄 Generating presentation for {company_name}...")

        # Title slide
        self.add_title_slide(
            company_name,
            config.get('subtitle', 'Agentic AI Journey')
        )

        # Add configured slides
        for slide_config in config.get('slides', []):
            if slide_config['type'] == 'diagram':
                self.add_diagram_slide(
                    slide_config['title'],
                    slide_config['image'],
                    slide_config.get('subtitle', '')
                )
            elif slide_config['type'] == 'content':
                self.add_content_slide(
                    slide_config['title'],
                    slide_config['content']
                )

        # Save
        self.prs.save(output_file)
        file_size = os.path.getsize(output_file) / 1024 / 1024

        print(f"   ✅ Generated: {output_file}")
        print(f"   📊 Slides: {len(self.prs.slides)}")
        print(f"   💾 Size: {file_size:.2f} MB")

        return output_file


# Example: Generate for Energy Australia
def generate_energy_australia_pptx():
    """Example: Generate EA presentation using generic system"""
    gen = AgenticAIPPTXGenerator()

    config = {
        "subtitle": "Agentic AI Journey\nTransformation Roadmap 2025-2026",
        "slides": [
            {
                "type": "diagram",
                "title": "Agentic AI Journey - 4 Phase Transformation",
                "image": "ea_journey_generic.png",
                "subtitle": "Traditional → Predictive → Augmented → Agentic"
            },
            {
                "type": "content",
                "title": "Journey Phases",
                "content": [
                    "• Phase 1: Traditional Analytics (Current)",
                    "  - Historical data, static BI, basic ML",
                    "",
                    "• Phase 2: Predictive AI (Q1-Q2 2025)",
                    "  - Delta Lake, MLflow, demand forecasting",
                    "",
                    "• Phase 3: Augmented AI (Q3-Q4 2025)",
                    "  - Unity Catalog, Mosaic AI, human-in-loop",
                    "",
                    "• Phase 4: Agentic AI (2026)",
                    "  - Autonomous agents with MCP protocol"
                ]
            },
            {
                "type": "diagram",
                "title": "Full Agentic AI Platform Architecture",
                "image": "ea_architecture_generic.png",
                "subtitle": "End-to-end platform with AI agents"
            },
            {
                "type": "diagram",
                "title": "Customer Service Agent - Autonomous Support",
                "image": "ea_customer_service_generic.png",
                "subtitle": "70% automation rate, 50% faster response"
            },
            {
                "type": "content",
                "title": "Business Impact & ROI",
                "content": [
                    "• Investment: $6.75M over 3 years",
                    "",
                    "• Annual Benefits (Year 3): $19M",
                    "  - Customer service cost reduction: $6M",
                    "  - Energy optimization savings: $5M",
                    "  - Churn reduction: $3M",
                    "  - Grid infrastructure: $3M",
                    "",
                    "• ROI Metrics:",
                    "  - Payback period: 15 months",
                    "  - 3-year ROI: 180%",
                    "  - 5-year NPV: $42M"
                ]
            }
        ]
    }

    return gen.generate_presentation(
        "Energy Australia",
        config,
        "Energy_Australia_Generic.pptx"
    )


if __name__ == "__main__":
    print("=" * 80)
    print("GENERIC AGENTIC AI PPTX GENERATOR")
    print("=" * 80)
    print("\nThis generator works for ANY company!")
    print("Just provide company name and configuration.")
    print("\nGenerating Energy Australia example...\n")

    generate_energy_australia_pptx()

    print("\n" + "=" * 80)
    print("✅ DONE! You can now use this for ANY company:")
    print("=" * 80)
    print("""
# Example for different company:
gen = AgenticAIPPTXGenerator()
config = {
    "subtitle": "Your Custom Subtitle",
    "slides": [
        {"type": "diagram", "title": "...", "image": "your_diagram.png"},
        {"type": "content", "title": "...", "content": ["...", "..."]}
    ]
}
gen.generate_presentation("Your Company Name", config, "output.pptx")
""")
