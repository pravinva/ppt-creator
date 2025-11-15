"""
Professional Databricks Architecture Diagram Generator
Draws like a real Databricks Solutions Architect

Uses PIL to create professional swim-lane diagrams with:
- Horizontal swim lanes (Source → Ingest → Process → Serve → Consume)
- Proper arrows showing data flow
- Clean boxes and labels
- Authentic Databricks 112x112 icons
- Modern 2025 style guide compliance
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os


class ProfessionalArchitectDiagramGenerator:
    """
    Draw professional Databricks architecture diagrams
    Like a real Solutions Architect would create
    """

    # Databricks 2025 color palette (RGB tuples)
    COLORS = {
        'dark_navy': (27, 49, 57),      # #1B3139
        'medium_blue': (27, 81, 98),    # #1B5162
        'light_blue': (97, 135, 148),   # #618794
        'orange': (255, 54, 33),        # #FF3621
        'yellow': (255, 171, 0),        # #FFAB00
        'green': (0, 169, 114),         # #00A972
        'white': (255, 255, 255),
        'light_gray': (239, 239, 239),  # #EFEFEF
        'gray': (217, 217, 217),        # #D9D9D9
        'text_gray': (102, 102, 102),   # #666666
        'bronze': (205, 127, 50),       # #CD7F32
        'silver': (192, 192, 192),      # #C0C0C0
        'gold': (255, 215, 0),          # #FFD700
    }

    def __init__(self, icons_dir="databricks_assets"):
        """Initialize with Databricks icons directory"""
        self.icons_dir = Path(icons_dir)
        self.icon_cache = {}

    def _load_icon(self, icon_name, size=80):
        """
        Load and resize Databricks icon

        Args:
            icon_name: Name like 'delta_lake', 's3_storage', etc.
            size: Target size (default 80px for diagrams)

        Returns:
            PIL Image or None
        """
        # Map icon names to files
        icon_map = {
            'databricks_sql': 'template_s024_i00.png',
            'delta_lake': 'template_s024_i01.png',
            'autoloader': 'template_s024_i02.png',
            'mlflow': 'template_s024_i03.png',
            'unity_catalog': 'template_s024_i04.png',
            'mosaic_ai': 'template_s024_i05.png',
            'feature_store': 'template_s024_i06.png',
            'workflows': 'template_s024_i07.png',
            'sql_warehouse': 'template_s024_i08.png',
            's3': 'template_s026_i00.png',
            'azure_blob': 'template_s026_i01.png',
            'kafka': 'template_s026_i03.png',
            'tableau': 'template_s027_i00.png',
            'powerbi': 'template_s027_i01.png',
        }

        cache_key = f"{icon_name}_{size}"
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]

        icon_file = icon_map.get(icon_name)
        if not icon_file:
            return None

        icon_path = self.icons_dir / icon_file
        if not icon_path.exists():
            return None

        try:
            icon = Image.open(icon_path)
            # Resize to target size maintaining aspect ratio
            icon.thumbnail((size, size), Image.Resampling.LANCZOS)
            self.icon_cache[cache_key] = icon
            return icon
        except:
            return None

    def _draw_rounded_rectangle(self, draw, xy, radius=10, fill=None, outline=None, width=1):
        """Draw a rounded rectangle"""
        x1, y1, x2, y2 = xy

        # Draw main rectangle
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=0)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=0)

        # Draw corners
        draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill, outline=outline, width=0)
        draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill, outline=outline, width=0)
        draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill, outline=outline, width=0)
        draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill, outline=outline, width=0)

        # Draw outline if specified
        if outline and width > 0:
            draw.arc([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=outline, width=width)
            draw.arc([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=outline, width=width)
            draw.arc([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=outline, width=width)
            draw.arc([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=outline, width=width)
            draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
            draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
            draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
            draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)

    def _draw_arrow(self, draw, x1, y1, x2, y2, color, width=2):
        """Draw an arrow from (x1, y1) to (x2, y2)"""
        # Draw line
        draw.line([x1, y1, x2, y2], fill=color, width=width)

        # Draw arrowhead
        import math
        arrow_length = 12
        arrow_angle = 25  # degrees

        angle = math.atan2(y2 - y1, x2 - x1)

        # Left side of arrowhead
        left_x = x2 - arrow_length * math.cos(angle - math.radians(arrow_angle))
        left_y = y2 - arrow_length * math.sin(angle - math.radians(arrow_angle))

        # Right side of arrowhead
        right_x = x2 - arrow_length * math.cos(angle + math.radians(arrow_angle))
        right_y = y2 - arrow_length * math.sin(angle + math.radians(arrow_angle))

        # Draw arrowhead triangle
        draw.polygon([
            (x2, y2),
            (left_x, left_y),
            (right_x, right_y)
        ], fill=color)

    def _get_text_size(self, text, font_size=14):
        """Get text bounding box size"""
        # Create temporary image to measure text
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = temp_draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def generate_medallion_architecture(
        self,
        company_name="Databricks",
        output_file="professional_medallion.png"
    ):
        """
        Generate professional medallion architecture diagram
        With proper swim lanes and data flow arrows
        """
        print(f"\n🎨 Drawing Professional Medallion Architecture for {company_name}...")

        # Canvas size
        width, height = 1400, 800
        img = Image.new('RGB', (width, height), self.COLORS['white'])
        draw = ImageDraw.Draw(img)

        # Load font
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            heading_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except:
            title_font = heading_font = label_font = small_font = ImageFont.load_default()

        # Title
        title = f"{company_name} - Medallion Architecture"
        draw.text((30, 30), title, fill=self.COLORS['dark_navy'], font=title_font)

        # Define swim lanes (vertical columns)
        margin_top = 100
        margin_left = 50
        lane_width = 250
        lane_height = 600
        spacing = 20

        lanes = [
            {"name": "Data Sources", "x": margin_left, "color": self.COLORS['light_gray']},
            {"name": "Bronze\n(Raw)", "x": margin_left + lane_width + spacing, "color": (255, 248, 240)},
            {"name": "Silver\n(Cleansed)", "x": margin_left + 2 * (lane_width + spacing), "color": (248, 248, 248)},
            {"name": "Gold\n(Business)", "x": margin_left + 3 * (lane_width + spacing), "color": (255, 250, 240)},
            {"name": "Consumption", "x": margin_left + 4 * (lane_width + spacing), "color": self.COLORS['light_gray']},
        ]

        # Draw swim lanes
        for i, lane in enumerate(lanes):
            x = lane['x']
            y = margin_top

            # Lane background
            self._draw_rounded_rectangle(
                draw,
                [x, y, x + lane_width, y + lane_height],
                radius=8,
                fill=lane['color'],
                outline=self.COLORS['gray'],
                width=1
            )

            # Lane title
            title_y = y + 15
            title_lines = lane['name'].split('\n')
            for line_idx, line in enumerate(title_lines):
                line_y = title_y + line_idx * 20
                text_width = self._get_text_size(line, 16)[0]
                draw.text((x + (lane_width - text_width) // 2, line_y), line,
                         fill=self.COLORS['dark_navy'], font=heading_font)

        # Components in each lane
        icon_y_start = margin_top + 80

        # Lane 1: Data Sources
        sources = [
            {"icon": "s3", "label": "Cloud\nStorage"},
            {"icon": "kafka", "label": "Streaming\nData"},
            {"icon": "azure_blob", "label": "Databases"}
        ]

        source_positions = []
        for idx, source in enumerate(sources):
            x = lanes[0]['x'] + lane_width // 2
            y = icon_y_start + idx * 150

            icon = self._load_icon(source['icon'], size=60)
            if icon:
                icon_x = x - icon.width // 2
                icon_y = y
                img.paste(icon, (icon_x, icon_y), icon if icon.mode == 'RGBA' else None)

            label_y = y + 70
            label_lines = source['label'].split('\n')
            for line_idx, line in enumerate(label_lines):
                line_y = label_y + line_idx * 16
                text_width = self._get_text_size(line, 13)[0]
                draw.text((x - text_width // 2, line_y), line,
                         fill=self.COLORS['text_gray'], font=label_font)

            source_positions.append((x + 30, y + 30))

        # Lane 2: Bronze
        bronze_x = lanes[1]['x'] + lane_width // 2
        bronze_y = icon_y_start + 150

        # AutoLoader icon
        autoloader_icon = self._load_icon('autoloader', size=70)
        if autoloader_icon:
            img.paste(autoloader_icon, (bronze_x - 35, bronze_y - 80),
                     autoloader_icon if autoloader_icon.mode == 'RGBA' else None)
        text_width = self._get_text_size("AutoLoader", 13)[0]
        draw.text((bronze_x - text_width // 2, bronze_y - 10), "AutoLoader",
                 fill=self.COLORS['text_gray'], font=label_font)

        # Delta Lake Bronze
        delta_icon = self._load_icon('delta_lake', size=70)
        if delta_icon:
            img.paste(delta_icon, (bronze_x - 35, bronze_y + 80),
                     delta_icon if delta_icon.mode == 'RGBA' else None)
        bronze_label_lines = ["Delta Lake", "Bronze"]
        for line_idx, line in enumerate(bronze_label_lines):
            line_y = bronze_y + 160 + line_idx * 20
            text_width = self._get_text_size(line, 16)[0]
            draw.text((bronze_x - text_width // 2, line_y), line,
                     fill=self.COLORS['bronze'], font=heading_font)

        bronze_pos = (bronze_x, bronze_y + 120)

        # Lane 3: Silver
        silver_x = lanes[2]['x'] + lane_width // 2
        silver_y = icon_y_start + 150

        if delta_icon:
            img.paste(delta_icon, (silver_x - 35, silver_y + 80),
                     delta_icon if delta_icon.mode == 'RGBA' else None)
        silver_label_lines = ["Delta Lake", "Silver"]
        for line_idx, line in enumerate(silver_label_lines):
            line_y = silver_y + 160 + line_idx * 20
            text_width = self._get_text_size(line, 16)[0]
            draw.text((silver_x - text_width // 2, line_y), line,
                     fill=self.COLORS['silver'], font=heading_font)

        # Unity Catalog
        uc_icon = self._load_icon('unity_catalog', size=50)
        if uc_icon:
            img.paste(uc_icon, (silver_x - 25, silver_y - 60),
                     uc_icon if uc_icon.mode == 'RGBA' else None)
        text_width = self._get_text_size("Unity Catalog", 11)[0]
        draw.text((silver_x - text_width // 2, silver_y - 10), "Unity Catalog",
                 fill=self.COLORS['text_gray'], font=small_font)

        silver_pos = (silver_x, silver_y + 120)

        # Lane 4: Gold
        gold_x = lanes[3]['x'] + lane_width // 2
        gold_y = icon_y_start + 150

        if delta_icon:
            img.paste(delta_icon, (gold_x - 35, gold_y + 80),
                     delta_icon if delta_icon.mode == 'RGBA' else None)
        gold_label_lines = ["Delta Lake", "Gold"]
        for line_idx, line in enumerate(gold_label_lines):
            line_y = gold_y + 160 + line_idx * 20
            text_width = self._get_text_size(line, 16)[0]
            draw.text((gold_x - text_width // 2, line_y), line,
                     fill=self.COLORS['gold'], font=heading_font)

        gold_pos = (gold_x, gold_y + 120)

        # Lane 5: Consumption
        consumers = [
            {"icon": "databricks_sql", "label": "Databricks SQL"},
            {"icon": "mosaic_ai", "label": "Mosaic AI GenAI"},
            {"icon": "tableau", "label": "BI Tools"}
        ]

        consumer_positions = []
        for idx, consumer in enumerate(consumers):
            x = lanes[4]['x'] + lane_width // 2
            y = icon_y_start + idx * 150

            icon = self._load_icon(consumer['icon'], size=60)
            if icon:
                icon_x = x - icon.width // 2
                icon_y = y
                img.paste(icon, (icon_x, icon_y), icon if icon.mode == 'RGBA' else None)

            label_y = y + 70
            label_lines = consumer['label'].split()
            for line_idx, line in enumerate(label_lines):
                line_y = label_y + line_idx * 16
                text_width = self._get_text_size(line, 13)[0]
                draw.text((x - text_width // 2, line_y), line,
                         fill=self.COLORS['text_gray'], font=label_font)

            consumer_positions.append((x - 30, y + 30))

        # Draw arrows showing data flow
        # Sources to Bronze
        for src_pos in source_positions:
            self._draw_arrow(
                draw,
                src_pos[0], src_pos[1],
                bronze_pos[0] - 80, bronze_pos[1],
                self.COLORS['light_blue'],
                width=3
            )

        # Bronze to Silver
        self._draw_arrow(
            draw,
            bronze_pos[0] + 80, bronze_pos[1],
            silver_pos[0] - 80, silver_pos[1],
            self.COLORS['medium_blue'],
            width=3
        )
        cleanse_lines = ["Cleanse &", "Validate"]
        for line_idx, line in enumerate(cleanse_lines):
            draw.text((bronze_pos[0] + 100, bronze_pos[1] - 20 + line_idx * 14), line,
                     fill=self.COLORS['medium_blue'], font=small_font)

        # Silver to Gold
        self._draw_arrow(
            draw,
            silver_pos[0] + 80, silver_pos[1],
            gold_pos[0] - 80, gold_pos[1],
            self.COLORS['medium_blue'],
            width=3
        )
        aggregate_lines = ["Aggregate &", "Transform"]
        for line_idx, line in enumerate(aggregate_lines):
            draw.text((silver_pos[0] + 100, silver_pos[1] - 20 + line_idx * 14), line,
                     fill=self.COLORS['medium_blue'], font=small_font)

        # Gold to Consumers
        for cons_pos in consumer_positions:
            self._draw_arrow(
                draw,
                gold_pos[0] + 80, gold_pos[1],
                cons_pos[0], cons_pos[1],
                self.COLORS['orange'],
                width=3
            )

        # Resize to max 1000px
        if width > 1000 or height > 1000:
            scale = min(1000 / width, 1000 / height)
            new_size = (int(width * scale), int(height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        img.save(output_file)
        print(f"   ✅ Saved: {output_file} ({img.width}x{img.height}px)")
        return output_file


def test_professional_generator():
    """Test the professional diagram generator"""
    print("=" * 80)
    print("PROFESSIONAL DATABRICKS ARCHITECTURE DIAGRAM GENERATOR")
    print("=" * 80)
    print("\nDrawing like a real Solutions Architect...")

    gen = ProfessionalArchitectDiagramGenerator()

    # Generate professional medallion
    gen.generate_medallion_architecture(
        "Energy Australia",
        "professional_ea_medallion.png"
    )

    print("\n" + "=" * 80)
    print("✅ PROFESSIONAL DIAGRAM GENERATED!")
    print("=" * 80)
    print("\nKey Improvements:")
    print("  ✓ Proper swim lanes (vertical columns)")
    print("  ✓ Real arrows showing data flow")
    print("  ✓ Professional layout and spacing")
    print("  ✓ Authentic Databricks 112x112 icons")
    print("  ✓ Modern 2025 color scheme")
    print("  ✓ Clean labels and typography")
    print("  ✓ Rounded rectangles and professional styling")


if __name__ == "__main__":
    test_professional_generator()
