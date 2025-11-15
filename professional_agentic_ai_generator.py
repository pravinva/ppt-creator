"""
Professional Generic Agentic AI Architecture Generator
Works for ANY company with professional swim-lane diagrams

Combines:
- Generic/configurable architecture (works for any company)
- Professional diagram drawing (like a real Solutions Architect)
- PIL-based rendering with proper arrows and swim lanes
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os


class ProfessionalAgenticAIGenerator:
    """
    Professional generic Agentic AI architecture generator
    Works for any company with proper swim-lane diagrams
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
        'phase1': (102, 102, 102),      # Gray for traditional
        'phase2': (27, 81, 98),         # Blue for predictive
        'phase3': (97, 135, 148),       # Light blue for augmented
        'phase4': (255, 54, 33),        # Orange for agentic
    }

    def __init__(self, icons_dir="databricks_assets"):
        """Initialize with Databricks icons directory"""
        self.icons_dir = Path(icons_dir)
        self.icon_cache = {}

        # Icon mapping
        self.icon_map = {
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
            's3_storage': 'template_s026_i00.png',
            'azure_blob': 'template_s026_i01.png',
            'kafka': 'template_s026_i03.png',
            'tableau': 'template_s027_i00.png',
            'powerbi': 'template_s027_i01.png',
            'default': 'template_s023_i16.png',
        }

    def _load_icon(self, icon_name, size=60):
        """Load and resize Databricks icon"""
        cache_key = f"{icon_name}_{size}"
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]

        icon_file = self.icon_map.get(icon_name, self.icon_map['default'])
        icon_path = self.icons_dir / icon_file

        if not icon_path.exists():
            return None

        try:
            icon = Image.open(icon_path)
            icon.thumbnail((size, size), Image.Resampling.LANCZOS)
            self.icon_cache[cache_key] = icon
            return icon
        except:
            return None

    def _get_text_size(self, text, font_size=14):
        """Get text bounding box size"""
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = temp_draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

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
        import math

        # Draw line
        draw.line([x1, y1, x2, y2], fill=color, width=width)

        # Draw arrowhead
        arrow_length = 12
        arrow_angle = 25

        angle = math.atan2(y2 - y1, x2 - x1)

        left_x = x2 - arrow_length * math.cos(angle - math.radians(arrow_angle))
        left_y = y2 - arrow_length * math.sin(angle - math.radians(arrow_angle))

        right_x = x2 - arrow_length * math.cos(angle + math.radians(arrow_angle))
        right_y = y2 - arrow_length * math.sin(angle + math.radians(arrow_angle))

        draw.polygon([
            (x2, y2),
            (left_x, left_y),
            (right_x, right_y)
        ], fill=color)

    def generate_journey_diagram(
        self,
        company_name: str,
        phase_descriptions: dict,
        output_file: str = "agentic_journey.png"
    ):
        """
        Generate 4-phase agentic AI journey diagram with professional styling

        Args:
            company_name: Company name
            phase_descriptions: Dict with phase configurations
            output_file: Output filename

        Example:
            phase_descriptions = {
                "Phase 1": {
                    "title": "Traditional Analytics",
                    "timeline": "Current State",
                    "components": [
                        {"name": "Historical Data", "icon": "delta_lake"},
                        {"name": "BI Reports", "icon": "tableau"}
                    ]
                },
                ...
            }
        """
        print(f"\n📊 Generating Professional Journey Diagram for {company_name}...")

        # Canvas size
        width, height = 1600, 700
        img = Image.new('RGB', (width, height), self.COLORS['white'])
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            heading_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except:
            title_font = heading_font = label_font = small_font = ImageFont.load_default()

        # Title
        title = f"{company_name} - Agentic AI Journey"
        draw.text((30, 30), title, fill=self.COLORS['dark_navy'], font=title_font)

        # Define phase boxes (horizontal layout)
        margin_top = 120
        margin_left = 50
        phase_width = 350
        phase_height = 500
        spacing = 20

        phase_colors = [
            (245, 245, 245),  # Gray for Phase 1
            (240, 248, 255),  # Light blue for Phase 2
            (240, 255, 255),  # Lighter blue for Phase 3
            (255, 245, 245),  # Light orange for Phase 4
        ]

        border_colors = [
            self.COLORS['phase1'],
            self.COLORS['phase2'],
            self.COLORS['phase3'],
            self.COLORS['phase4'],
        ]

        phase_x_positions = []

        # Draw phases
        for idx, (phase_name, phase_info) in enumerate(phase_descriptions.items()):
            x = margin_left + idx * (phase_width + spacing)
            y = margin_top

            # Phase box
            self._draw_rounded_rectangle(
                draw,
                [x, y, x + phase_width, y + phase_height],
                radius=8,
                fill=phase_colors[idx],
                outline=border_colors[idx],
                width=2
            )

            # Phase title
            phase_title = f"{phase_name}: {phase_info['title']}"
            title_width = self._get_text_size(phase_title, 16)[0]
            draw.text((x + (phase_width - title_width) // 2, y + 15), phase_title,
                     fill=border_colors[idx], font=heading_font)

            # Timeline
            timeline = phase_info.get('timeline', '')
            timeline_width = self._get_text_size(timeline, 11)[0]
            draw.text((x + (phase_width - timeline_width) // 2, y + 40), timeline,
                     fill=self.COLORS['text_gray'], font=small_font)

            # Components
            components = phase_info.get('components', [])
            comp_y = y + 80

            for comp_idx, component in enumerate(components):
                if isinstance(component, dict):
                    comp_name = component['name']
                    icon_name = component.get('icon', 'default')
                else:
                    comp_name = component
                    # Auto-map icon from component name
                    icon_name = comp_name.lower().replace(' ', '_')

                # Icon
                icon = self._load_icon(icon_name, size=50)
                if icon:
                    icon_x = x + (phase_width - icon.width) // 2
                    icon_y = comp_y + comp_idx * 100
                    img.paste(icon, (icon_x, icon_y), icon if icon.mode == 'RGBA' else None)

                    # Label
                    label_y = icon_y + 60
                    label_width = self._get_text_size(comp_name, 13)[0]
                    draw.text((x + (phase_width - label_width) // 2, label_y), comp_name,
                             fill=self.COLORS['text_gray'], font=label_font)

            phase_x_positions.append(x + phase_width // 2)

        # Draw arrows between phases
        arrow_y = margin_top + phase_height // 2
        for i in range(len(phase_x_positions) - 1):
            x1 = phase_x_positions[i] + phase_width // 2
            x2 = phase_x_positions[i + 1] - phase_width // 2

            self._draw_arrow(
                draw,
                x1, arrow_y,
                x2, arrow_y,
                self.COLORS['medium_blue'],
                width=3
            )

        # Resize to max 1000px
        if width > 1000:
            scale = 1000 / width
            new_size = (int(width * scale), int(height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        img.save(output_file)
        print(f"   ✅ Saved: {output_file} ({img.width}x{img.height}px)")
        return output_file

    def generate_full_architecture(
        self,
        company_name: str,
        architecture_config: dict,
        output_file: str = "agentic_architecture.png"
    ):
        """
        Generate professional full architecture with swim lanes

        Args:
            company_name: Company name
            architecture_config: Configuration with layers
            output_file: Output filename

        Example:
            architecture_config = {
                "data_sources": [
                    {"name": "Smart Meters", "icon": "s3"}
                ],
                "platform_components": [
                    {"name": "Delta Lake", "icon": "delta_lake"}
                ],
                "ai_agents": [
                    {"name": "Customer Agent", "icon": "mosaic_ai"}
                ],
                "applications": [
                    {"name": "Web Portal", "icon": "tableau"}
                ]
            }
        """
        print(f"\n🏗️  Generating Professional Architecture for {company_name}...")

        # Canvas size
        width, height = 1600, 800
        img = Image.new('RGB', (width, height), self.COLORS['white'])
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            heading_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        except:
            title_font = heading_font = label_font = ImageFont.load_default()

        # Title
        title = f"{company_name} - Agentic AI Platform"
        draw.text((30, 30), title, fill=self.COLORS['dark_navy'], font=title_font)

        # Define swim lanes
        margin_top = 100
        margin_left = 50
        lane_width = 350
        lane_height = 600
        spacing = 20

        lanes = [
            {"name": "Data Sources", "color": self.COLORS['light_gray']},
            {"name": "Databricks Platform", "color": (240, 248, 255)},
            {"name": "AI Agents", "color": (255, 245, 245)},
            {"name": "Applications", "color": self.COLORS['light_gray']},
        ]

        # Draw swim lanes
        for i, lane in enumerate(lanes):
            x = margin_left + i * (lane_width + spacing)
            y = margin_top

            self._draw_rounded_rectangle(
                draw,
                [x, y, x + lane_width, y + lane_height],
                radius=8,
                fill=lane['color'],
                outline=self.COLORS['gray'],
                width=1
            )

            # Lane title
            title_width = self._get_text_size(lane['name'], 16)[0]
            draw.text((x + (lane_width - title_width) // 2, y + 15), lane['name'],
                     fill=self.COLORS['dark_navy'], font=heading_font)

        # Add components to lanes
        icon_y_start = margin_top + 80

        # Lane 0: Data Sources
        if 'data_sources' in architecture_config:
            sources = architecture_config['data_sources']
            for idx, source in enumerate(sources[:3]):  # Max 3
                x = margin_left + lane_width // 2
                y = icon_y_start + idx * 140

                icon = self._load_icon(source.get('icon', 'default'), size=60)
                if icon:
                    img.paste(icon, (x - icon.width // 2, y),
                             icon if icon.mode == 'RGBA' else None)

                label_y = y + 70
                label_width = self._get_text_size(source['name'], 13)[0]
                draw.text((x - label_width // 2, label_y), source['name'],
                         fill=self.COLORS['text_gray'], font=label_font)

        # Lane 1: Platform Components
        if 'platform_components' in architecture_config:
            components = architecture_config['platform_components']
            for idx, comp in enumerate(components[:4]):  # Max 4
                x = margin_left + lane_width + spacing + lane_width // 2
                y = icon_y_start + idx * 120

                icon = self._load_icon(comp.get('icon', 'default'), size=60)
                if icon:
                    img.paste(icon, (x - icon.width // 2, y),
                             icon if icon.mode == 'RGBA' else None)

                label_y = y + 70
                label_width = self._get_text_size(comp['name'], 13)[0]
                draw.text((x - label_width // 2, label_y), comp['name'],
                         fill=self.COLORS['text_gray'], font=label_font)

        # Lane 2: AI Agents
        if 'ai_agents' in architecture_config:
            agents = architecture_config['ai_agents']
            for idx, agent in enumerate(agents[:3]):  # Max 3
                x = margin_left + 2 * (lane_width + spacing) + lane_width // 2
                y = icon_y_start + idx * 140

                icon = self._load_icon(agent.get('icon', 'mosaic_ai'), size=60)
                if icon:
                    img.paste(icon, (x - icon.width // 2, y),
                             icon if icon.mode == 'RGBA' else None)

                label_y = y + 70
                label_width = self._get_text_size(agent['name'], 13)[0]
                draw.text((x - label_width // 2, label_y), agent['name'],
                         fill=self.COLORS['text_gray'], font=label_font)

        # Lane 3: Applications
        if 'applications' in architecture_config:
            apps = architecture_config['applications']
            for idx, app in enumerate(apps[:3]):  # Max 3
                x = margin_left + 3 * (lane_width + spacing) + lane_width // 2
                y = icon_y_start + idx * 140

                icon = self._load_icon(app.get('icon', 'default'), size=60)
                if icon:
                    img.paste(icon, (x - icon.width // 2, y),
                             icon if icon.mode == 'RGBA' else None)

                label_y = y + 70
                label_width = self._get_text_size(app['name'], 13)[0]
                draw.text((x - label_width // 2, label_y), app['name'],
                         fill=self.COLORS['text_gray'], font=label_font)

        # Draw flow arrows between lanes
        arrow_y = margin_top + lane_height // 2
        for i in range(len(lanes) - 1):
            x1 = margin_left + i * (lane_width + spacing) + lane_width
            x2 = margin_left + (i + 1) * (lane_width + spacing)

            self._draw_arrow(
                draw,
                x1, arrow_y,
                x2, arrow_y,
                self.COLORS['medium_blue'],
                width=3
            )

        # Resize to max 1000px
        if width > 1000:
            scale = 1000 / width
            new_size = (int(width * scale), int(height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        img.save(output_file)
        print(f"   ✅ Saved: {output_file} ({img.width}x{img.height}px)")
        return output_file


# Example usage for Energy Australia
def generate_energy_australia_professional():
    """Generate Energy Australia diagrams using professional generic system"""
    gen = ProfessionalAgenticAIGenerator()

    print("=" * 80)
    print("PROFESSIONAL GENERIC AGENTIC AI GENERATOR - ENERGY AUSTRALIA")
    print("=" * 80)

    # 1. Journey Diagram
    ea_journey = {
        "Phase 1": {
            "title": "Traditional",
            "timeline": "Current State",
            "components": [
                {"name": "Historical Data", "icon": "delta_lake"},
                {"name": "BI Reports", "icon": "tableau"},
                {"name": "Basic ML", "icon": "mlflow"}
            ]
        },
        "Phase 2": {
            "title": "Predictive AI",
            "timeline": "Q1-Q2 2025",
            "components": [
                {"name": "Delta Lake", "icon": "delta_lake"},
                {"name": "MLflow", "icon": "mlflow"},
                {"name": "Model Serving", "icon": "workflows"}
            ]
        },
        "Phase 3": {
            "title": "Augmented AI",
            "timeline": "Q3-Q4 2025",
            "components": [
                {"name": "Unity Catalog", "icon": "unity_catalog"},
                {"name": "Mosaic AI", "icon": "mosaic_ai"},
                {"name": "Feature Store", "icon": "feature_store"}
            ]
        },
        "Phase 4": {
            "title": "Agentic AI",
            "timeline": "2026",
            "components": [
                {"name": "AI Agents", "icon": "mosaic_ai"},
                {"name": "MCP Protocol", "icon": "workflows"},
                {"name": "Autonomous", "icon": "mosaic_ai"}
            ]
        }
    }

    gen.generate_journey_diagram(
        "Energy Australia",
        ea_journey,
        "ea_journey_professional.png"
    )

    # 2. Full Architecture
    ea_architecture = {
        "data_sources": [
            {"name": "Smart Meters", "icon": "s3"},
            {"name": "CRM System", "icon": "azure_blob"},
            {"name": "Grid Data", "icon": "kafka"}
        ],
        "platform_components": [
            {"name": "AutoLoader", "icon": "autoloader"},
            {"name": "Delta Lake", "icon": "delta_lake"},
            {"name": "Unity Catalog", "icon": "unity_catalog"},
            {"name": "Mosaic AI", "icon": "mosaic_ai"}
        ],
        "ai_agents": [
            {"name": "Customer Service", "icon": "mosaic_ai"},
            {"name": "Energy Optimization", "icon": "mosaic_ai"},
            {"name": "Grid Management", "icon": "mosaic_ai"}
        ],
        "applications": [
            {"name": "Customer Portal", "icon": "tableau"},
            {"name": "Mobile App", "icon": "powerbi"}
        ]
    }

    gen.generate_full_architecture(
        "Energy Australia",
        ea_architecture,
        "ea_architecture_professional.png"
    )

    print("\n" + "=" * 80)
    print("✅ PROFESSIONAL DIAGRAMS GENERATED!")
    print("=" * 80)
    print("\nYou can now generate for ANY company by calling:")
    print("  gen.generate_journey_diagram('Your Company', journey_config, 'output.png')")
    print("  gen.generate_full_architecture('Your Company', arch_config, 'output.png')")


if __name__ == "__main__":
    generate_energy_australia_professional()
