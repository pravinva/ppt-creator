"""
Energy Australia Agentic AI Journey - PowerPoint Generator
Creates a professional PPTX presentation with all architecture diagrams
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from PIL import Image
import os


class EnergyAustraliaPPTXGenerator:
    """Generate Energy Australia Agentic AI presentation"""

    # Modern Databricks 2025 colors
    NAVY = RGBColor(27, 49, 57)         # #1B3139
    ORANGE = RGBColor(255, 54, 33)      # #FF3621
    LIGHT_BLUE = RGBColor(97, 135, 148) # #618794
    WHITE = RGBColor(255, 255, 255)
    LIGHT_GRAY = RGBColor(239, 239, 239)

    def __init__(self):
        """Initialize presentation with standard slide size"""
        self.prs = Presentation()
        self.prs.slide_width = Inches(10)
        self.prs.slide_height = Inches(7.5)

    def add_title_slide(self):
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

        # Orange accent bar at top
        accent = slide.shapes.add_shape(
            1, 0, 0, self.prs.slide_width, Inches(0.4)
        )
        accent.fill.solid()
        accent.fill.fore_color.rgb = self.ORANGE
        accent.line.color.rgb = self.ORANGE

        # Title
        title_box = slide.shapes.add_textbox(
            Inches(1), Inches(2.5), Inches(8), Inches(2)
        )
        title_frame = title_box.text_frame
        title_frame.text = "Energy Australia"

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
        subtitle_frame.text = "Agentic AI Journey\nTransformation Roadmap 2025-2026"

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

    def add_agenda_slide(self):
        """Add agenda/overview slide"""
        slide_layout = self.prs.slide_layouts[6]  # Blank
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
            Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)
        )
        title_frame = title_box.text_frame
        title_frame.text = "Agenda"

        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(44)
        title_para.font.bold = True
        title_para.font.color.rgb = self.NAVY

        # Content
        content_box = slide.shapes.add_textbox(
            Inches(1), Inches(1.8), Inches(8), Inches(5)
        )
        content_frame = content_box.text_frame

        agenda_items = [
            "1. Agentic AI Journey Overview",
            "   • 4-phase transformation roadmap",
            "   • Traditional → Predictive → Augmented → Agentic",
            "",
            "2. Full Platform Architecture",
            "   • End-to-end data and AI platform",
            "   • Model Context Protocol (MCP) integration",
            "",
            "3. Customer Service Agent",
            "   • Autonomous customer interactions",
            "   • 70% automation rate",
            "",
            "4. Energy Optimization Agent",
            "   • Real-time demand forecasting",
            "   • $5M annual savings",
            "",
            "5. Business Impact & ROI",
            "   • $19M annual benefits by 2026",
            "   • 180% three-year ROI"
        ]

        for item in agenda_items:
            p = content_frame.add_paragraph()
            p.text = item
            if item.startswith(('1.', '2.', '3.', '4.', '5.')):
                p.font.size = Pt(24)
                p.font.bold = True
                p.font.color.rgb = self.NAVY
                p.space_before = Pt(12)
            elif item.strip():
                p.font.size = Pt(18)
                p.font.color.rgb = self.LIGHT_BLUE
                p.level = 1

    def add_diagram_slide(self, title: str, image_path: str, subtitle: str = ""):
        """Add slide with diagram image"""
        if not os.path.exists(image_path):
            print(f"Warning: Image not found: {image_path}")
            return

        slide_layout = self.prs.slide_layouts[6]  # Blank
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

        # Subtitle if provided
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

        # Add diagram image
        # Calculate optimal size while maintaining aspect ratio
        img = Image.open(image_path)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        # Available space
        max_width = Inches(9)
        max_height = Inches(7.5) - top_offset - Inches(0.3)

        # Calculate size
        if aspect_ratio > (max_width / max_height):
            # Width-constrained
            width = max_width
            height = width / aspect_ratio
        else:
            # Height-constrained
            height = max_height
            width = height * aspect_ratio

        # Center horizontally
        left = (self.prs.slide_width - width) / 2

        slide.shapes.add_picture(image_path, left, top_offset, width=width)

    def add_content_slide(self, title: str, content: list, highlight_color=None):
        """Add text content slide"""
        slide_layout = self.prs.slide_layouts[6]  # Blank
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
            elif item.startswith('  -') or item.startswith('    •'):
                p.level = 1
                p.font.size = Pt(18)

    def add_roi_slide(self):
        """Add ROI and business impact slide"""
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
        title_frame.text = "Business Impact & ROI"

        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(36)
        title_para.font.bold = True
        title_para.font.color.rgb = self.NAVY

        # Left column - Investment
        left_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(1.5), Inches(4.5), Inches(5.5)
        )
        left_frame = left_box.text_frame

        investment_items = [
            "Investment (3-Year TCO)",
            "",
            "Year 1: $2.15M",
            "  • Databricks Platform: $500K",
            "  • Azure Infrastructure: $300K",
            "  • Data Engineering: $400K",
            "  • ML/AI Development: $600K",
            "",
            "Year 2: $2.25M",
            "Year 3: $2.35M",
            "",
            "Total: $6.75M"
        ]

        for item in investment_items:
            p = left_frame.add_paragraph()
            p.text = item
            if item.startswith('Investment') or item.startswith('Total'):
                p.font.size = Pt(22)
                p.font.bold = True
                p.font.color.rgb = self.ORANGE
            elif item.startswith(('Year', '  •')):
                p.font.size = Pt(18)
                p.font.color.rgb = self.NAVY
            elif item.strip():
                p.font.size = Pt(16)
                p.font.color.rgb = self.LIGHT_BLUE

        # Right column - Benefits
        right_box = slide.shapes.add_textbox(
            Inches(5.5), Inches(1.5), Inches(4), Inches(5.5)
        )
        right_frame = right_box.text_frame

        benefits_items = [
            "Annual Benefits (Year 3)",
            "",
            "Customer Service: $6M",
            "Energy Optimization: $5M",
            "Churn Reduction: $3M",
            "Grid Infrastructure: $3M",
            "Operational Efficiency: $2M",
            "",
            "Total: $19M/year",
            "",
            "ROI Metrics:",
            "  • Payback: 15 months",
            "  • 3-Year ROI: 180%",
            "  • 5-Year NPV: $42M"
        ]

        for item in benefits_items:
            p = right_frame.add_paragraph()
            p.text = item
            if item.startswith('Annual') or item.startswith('Total'):
                p.font.size = Pt(22)
                p.font.bold = True
                p.font.color.rgb = self.ORANGE
            elif item.startswith('ROI'):
                p.font.size = Pt(20)
                p.font.bold = True
                p.font.color.rgb = self.NAVY
            elif item.startswith('  •'):
                p.font.size = Pt(18)
                p.font.color.rgb = self.LIGHT_BLUE
            elif item.strip():
                p.font.size = Pt(18)
                p.font.color.rgb = self.NAVY

    def generate_complete_presentation(self):
        """Generate complete Energy Australia presentation"""
        print("=" * 80)
        print("GENERATING ENERGY AUSTRALIA AGENTIC AI PRESENTATION")
        print("=" * 80)

        # Slide 1: Title
        print("\n1. Adding title slide...")
        self.add_title_slide()

        # Slide 2: Agenda
        print("2. Adding agenda slide...")
        self.add_agenda_slide()

        # Slide 3: Journey Overview Diagram
        print("3. Adding journey overview diagram...")
        self.add_diagram_slide(
            "Agentic AI Journey - 4 Phase Transformation",
            "ea_agentic_journey.png",
            "Traditional → Predictive AI → Augmented AI → Agentic AI"
        )

        # Slide 4: Phase descriptions
        print("4. Adding phase descriptions...")
        self.add_content_slide(
            "Journey Phases",
            [
                "• Phase 1: Traditional Analytics (Current)",
                "  - Historical data analysis and static BI reports",
                "  - Basic ML models with limited deployment",
                "",
                "• Phase 2: Predictive AI (Q1-Q2 2025)",
                "  - Delta Lake unified platform on Azure",
                "  - MLflow model registry and serving",
                "  - Demand forecasting and churn prediction",
                "",
                "• Phase 3: Augmented AI (Q3-Q4 2025)",
                "  - Unity Catalog governance and Mosaic AI GenAI",
                "  - Feature Store and RAG implementation",
                "  - AI-assisted customer service (human-in-loop)",
                "",
                "• Phase 4: Agentic AI (2026)",
                "  - Fully autonomous AI agents with MCP",
                "  - 70% autonomous customer service handling",
                "  - Real-time energy optimization and grid control"
            ]
        )

        # Slide 5: Full Architecture Diagram
        print("5. Adding full architecture diagram...")
        self.add_diagram_slide(
            "Full Agentic AI Platform Architecture",
            "ea_agentic_architecture.png",
            "End-to-end platform from data sources to AI agents and applications"
        )

        # Slide 6: Architecture components
        print("6. Adding architecture components...")
        self.add_content_slide(
            "Platform Components",
            [
                "• Data Sources",
                "  - Smart Meters (IoT streaming), Customer CRM, Grid Operations, Weather Data",
                "",
                "• Databricks Lakehouse Platform",
                "  - AutoLoader streaming ingestion, Medallion architecture (Bronze/Silver/Gold)",
                "  - Unity Catalog governance, Delta Lake ACID storage",
                "",
                "• AI/ML Platform",
                "  - Feature Store for centralized features",
                "  - MLflow for model lifecycle management",
                "  - Mosaic AI GenAI platform with LLMs",
                "",
                "• Agentic AI Layer",
                "  - Agent Framework with MCP (Model Context Protocol)",
                "  - Customer Service, Energy Optimization, Grid Management Agents",
                "",
                "• Applications",
                "  - Customer Portal, Operations Dashboard, Mobile App"
            ]
        )

        # Slide 7: Customer Service Agent
        print("7. Adding customer service agent diagram...")
        self.add_diagram_slide(
            "Customer Service Agent - Autonomous Support",
            "ea_customer_agent.png",
            "Intent Understanding → Reasoning → Action Execution with MCP Context"
        )

        # Slide 8: Customer agent use case
        print("8. Adding customer agent use case...")
        self.add_content_slide(
            "Customer Service Agent - Use Case",
            [
                "• Customer Interaction Channels",
                "  - Web portal, mobile app, phone/IVR with natural language",
                "",
                "• Agent Processing Flow",
                "  - Intent Understanding: What does customer want?",
                "  - Reasoning & Planning: How to best serve request?",
                "  - Action Execution: Execute the solution autonomously",
                "",
                "• MCP Context Enrichment",
                "  - Customer profile (demographics, preferences)",
                "  - Usage history (consumption patterns, anomalies)",
                "  - Billing data (payment history, current balance)",
                "",
                "• Autonomous Outcomes",
                "  - Energy usage recommendations and insights",
                "  - Issue resolution (billing questions, outages)",
                "  - Usage optimization tips and plan adjustments",
                "",
                "• Impact: 70% automation rate, 50% faster response, 40% cost reduction"
            ]
        )

        # Slide 9: Energy Optimization Agent
        print("9. Adding energy optimization agent diagram...")
        self.add_diagram_slide(
            "Energy Optimization Agent - Real-Time Forecasting",
            "ea_optimization_agent.png",
            "Streaming data processing with autonomous demand prediction and grid control"
        )

        # Slide 10: Optimization agent use case
        print("10. Adding optimization agent use case...")
        self.add_content_slide(
            "Energy Optimization Agent - Use Case",
            [
                "• Real-Time Data Streams",
                "  - Smart meter data (15-min intervals)",
                "  - Weather forecasts (hourly updates)",
                "  - Grid load data (real-time SCADA)",
                "",
                "• Stream Processing",
                "  - AutoLoader for incremental ingestion",
                "  - Structured Streaming for real-time analytics",
                "  - Delta Live Tables for always-fresh data",
                "",
                "• Agent Actions",
                "  - Demand Prediction: 1-48 hour forecasting with ML",
                "  - Load Optimization: Grid balancing and peak shaving",
                "  - Customer Recommendations: Time-of-use pricing, smart scheduling",
                "",
                "• Automated Outcomes",
                "  - Dynamic Pricing: Adjust rates based on demand/supply",
                "  - Customer Alerts: Notify of high-cost periods",
                "  - Grid Control: Automated load balancing",
                "",
                "• Impact: 30% forecast improvement, $5M annual savings, 15% peak reduction"
            ]
        )

        # Slide 11: ROI
        print("11. Adding ROI slide...")
        self.add_roi_slide()

        # Slide 12: Next Steps
        print("12. Adding next steps...")
        self.add_content_slide(
            "Implementation Next Steps",
            [
                "• Q1 2025: Foundation & Data Platform",
                "  - Deploy Delta Lake on Azure ADLS Gen2",
                "  - Implement Medallion architecture (Bronze/Silver/Gold)",
                "  - Set up MLflow model registry and serving",
                "",
                "• Q2 2025: Predictive Models",
                "  - Build demand forecasting and churn prediction",
                "  - Deploy customer 360 view and personalization",
                "  - Production rollout with A/B testing",
                "",
                "• Q3-Q4 2025: GenAI & Governance",
                "  - Deploy Unity Catalog and Mosaic AI platform",
                "  - Implement RAG and LLM endpoints",
                "  - Build Feature Store and human-in-loop AI",
                "",
                "• Q1-Q2 2026: Agentic AI",
                "  - Deploy agent framework with MCP protocol",
                "  - Launch Customer Service and Energy Optimization agents",
                "  - Full production rollout with monitoring"
            ]
        )

        # Slide 13: Closing
        print("13. Adding closing slide...")
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)

        background = slide.shapes.add_shape(
            1, 0, 0, self.prs.slide_width, self.prs.slide_height
        )
        background.fill.solid()
        background.fill.fore_color.rgb = self.WHITE
        background.line.color.rgb = self.WHITE

        closing_box = slide.shapes.add_textbox(
            Inches(1), Inches(2.5), Inches(8), Inches(3)
        )
        closing_frame = closing_box.text_frame

        p1 = closing_frame.paragraphs[0]
        p1.text = "Questions?"
        p1.font.size = Pt(60)
        p1.font.bold = True
        p1.font.color.rgb = self.NAVY
        p1.alignment = PP_ALIGN.CENTER

        p2 = closing_frame.add_paragraph()
        p2.text = "\nReady to transform Energy Australia with Agentic AI"
        p2.font.size = Pt(28)
        p2.font.color.rgb = self.LIGHT_BLUE
        p2.alignment = PP_ALIGN.CENTER

        # Save presentation
        output_file = "Energy_Australia_Agentic_AI_Journey.pptx"
        self.prs.save(output_file)

        print("\n" + "=" * 80)
        print("✅ PRESENTATION GENERATED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nFile: {output_file}")
        print(f"Slides: {len(self.prs.slides)}")
        print(f"Size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
        print("\nPresentation includes:")
        print("  1. Title slide")
        print("  2. Agenda")
        print("  3. Journey Overview (4 phases)")
        print("  4. Phase descriptions")
        print("  5. Full architecture diagram")
        print("  6. Architecture components")
        print("  7. Customer Service Agent diagram")
        print("  8. Customer Service Agent use case")
        print("  9. Energy Optimization Agent diagram")
        print("  10. Energy Optimization Agent use case")
        print("  11. ROI and business impact")
        print("  12. Implementation roadmap")
        print("  13. Closing slide")

        return output_file


if __name__ == "__main__":
    generator = EnergyAustraliaPPTXGenerator()
    generator.generate_complete_presentation()
