"""
Diagram Generator for Databricks Architecture Diagrams
Creates medallion architecture and other Databricks-style diagrams
"""
from PIL import Image, ImageDraw, ImageFont
import io
from typing import Tuple


class DiagramGenerator:
    """Generate Databricks-style architecture diagrams"""

    # Databricks brand colors
    COLORS = {
        'databricks_red': '#FF3621',
        'databricks_dark': '#1B3139',
        'bronze': '#CD7F32',
        'silver': '#C0C0C0',
        'gold': '#FFD700',
        'white': '#FFFFFF',
        'light_gray': '#E8E8E8',
        'dark_gray': '#666666',
        'blue': '#00A4E4',
        'green': '#00C853',
    }

    def __init__(self, width: int = 1280, height: int = 720):
        """
        Initialize diagram generator

        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.width = width
        self.height = height

    def generate_medallion_architecture(self, description: str = None) -> Image.Image:
        """
        Generate a medallion architecture diagram

        Args:
            description: Optional description to customize the diagram

        Returns:
            PIL Image object
        """
        img = Image.new('RGB', (self.width, self.height), self.COLORS['white'])
        draw = ImageDraw.Draw(img)

        # Try to load a font, fallback to default if not available
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Draw title
        title = "Medallion Architecture"
        draw.text((40, 30), title, fill=self.COLORS['databricks_dark'], font=title_font)

        # Define layer positions
        layer_width = 280
        layer_height = 400
        spacing = 80
        start_x = 100
        start_y = 150

        # Bronze layer
        bronze_x = start_x
        self._draw_layer(
            draw,
            bronze_x, start_y,
            layer_width, layer_height,
            "Bronze",
            self.COLORS['bronze'],
            [
                "Raw Data",
                "Data Ingestion",
                "Source Systems",
                "Streaming & Batch"
            ],
            label_font,
            text_font
        )

        # Arrow
        self._draw_arrow(draw, bronze_x + layer_width, start_y + layer_height // 2,
                        bronze_x + layer_width + spacing, start_y + layer_height // 2)

        # Silver layer
        silver_x = bronze_x + layer_width + spacing
        self._draw_layer(
            draw,
            silver_x, start_y,
            layer_width, layer_height,
            "Silver",
            self.COLORS['silver'],
            [
                "Cleansed Data",
                "Validated",
                "Deduplicated",
                "Conformed"
            ],
            label_font,
            text_font
        )

        # Arrow
        self._draw_arrow(draw, silver_x + layer_width, start_y + layer_height // 2,
                        silver_x + layer_width + spacing, start_y + layer_height // 2)

        # Gold layer
        gold_x = silver_x + layer_width + spacing
        self._draw_layer(
            draw,
            gold_x, start_y,
            layer_width, layer_height,
            "Gold",
            self.COLORS['gold'],
            [
                "Business-Level",
                "Aggregated",
                "Feature Tables",
                "Analytics-Ready"
            ],
            label_font,
            text_font
        )

        return img

    def generate_architecture_diagram(self, description: str = None) -> Image.Image:
        """
        Generate a generic Databricks architecture diagram

        Args:
            description: Description to guide diagram generation

        Returns:
            PIL Image object
        """
        img = Image.new('RGB', (self.width, self.height), self.COLORS['white'])
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Draw title
        title = "Databricks Architecture"
        draw.text((40, 30), title, fill=self.COLORS['databricks_dark'], font=title_font)

        # Draw components in layers
        # Data Sources
        self._draw_box(draw, 100, 150, 250, 120, "Data Sources",
                      self.COLORS['blue'], label_font, text_font)

        # Databricks Lakehouse
        self._draw_box(draw, 450, 150, 380, 400, "Databricks Lakehouse",
                      self.COLORS['databricks_red'], label_font, text_font)

        # Analytics & ML
        self._draw_box(draw, 920, 150, 280, 120, "Analytics & ML",
                      self.COLORS['green'], label_font, text_font)

        # Draw arrows
        self._draw_arrow(draw, 350, 210, 450, 210)
        self._draw_arrow(draw, 830, 210, 920, 210)

        return img

    def _draw_layer(self, draw, x, y, width, height, title, color, items, label_font, text_font):
        """Draw a single medallion layer"""
        # Draw rounded rectangle
        radius = 20
        draw.rounded_rectangle(
            [(x, y), (x + width, y + height)],
            radius=radius,
            fill=color,
            outline=self.COLORS['databricks_dark'],
            width=3
        )

        # Draw title
        title_color = self.COLORS['databricks_dark'] if color == self.COLORS['gold'] else self.COLORS['white']
        draw.text((x + width // 2 - 50, y + 20), title, fill=title_color, font=label_font)

        # Draw items
        item_y = y + 80
        for item in items:
            draw.text((x + 20, item_y), f"• {item}", fill=title_color, font=text_font)
            item_y += 60

    def _draw_box(self, draw, x, y, width, height, label, color, label_font, text_font):
        """Draw a box with label"""
        draw.rounded_rectangle(
            [(x, y), (x + width, y + height)],
            radius=15,
            fill=color,
            outline=self.COLORS['databricks_dark'],
            width=3
        )
        # Center the text
        draw.text((x + 20, y + height // 2 - 15), label, fill=self.COLORS['white'], font=label_font)

    def _draw_arrow(self, draw, x1, y1, x2, y2):
        """Draw an arrow between two points"""
        # Arrow line
        draw.line([(x1, y1), (x2, y2)], fill=self.COLORS['databricks_dark'], width=4)

        # Arrow head
        arrow_size = 15
        draw.polygon([
            (x2, y2),
            (x2 - arrow_size, y2 - arrow_size // 2),
            (x2 - arrow_size, y2 + arrow_size // 2)
        ], fill=self.COLORS['databricks_dark'])

    def save_diagram(self, image: Image.Image, filepath: str):
        """Save diagram to file"""
        image.save(filepath, 'PNG')

    def get_image_bytes(self, image: Image.Image) -> bytes:
        """Convert image to bytes for embedding in PowerPoint"""
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr
