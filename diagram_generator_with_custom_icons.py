"""
Modern Databricks Diagram Generator with Custom Icons
Uses extracted 112x112 Databricks icons from databricks_assets/
Follows 2025 Databricks style guide
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os


class ModernDatabricksIconGenerator:
    """
    Generate diagrams using actual Databricks 112x112 icons
    from databricks_assets folder
    """

    # Modern Databricks 2025 color palette
    COLORS = {
        'dark_navy': '#1B3139',
        'medium_blue': '#1B5162',
        'light_blue': '#618794',
        'orange': '#FF3621',
        'yellow': '#FFAB00',
        'green': '#00A972',
        'white': '#FFFFFF',
        'bronze': '#CD7F32',
        'silver': '#C0C0C0',
        'gold': '#FFD700',
    }

    def __init__(self, icons_dir="databricks_assets"):
        """
        Initialize with path to extracted Databricks icons

        Args:
            icons_dir: Directory containing extracted Databricks icons
        """
        self.icons_dir = Path(icons_dir)
        self.icon_mapping = self._discover_icons()

    def _discover_icons(self):
        """
        Discover and catalog available Databricks icons

        Returns mapping of icon names to file paths
        """
        icon_map = {}

        # Databricks product icons (slide 24 from template)
        # These are the 112x112 standard icons
        for i in range(20):  # Check up to 20 icons
            icon_file = self.icons_dir / f"template_s024_i{i:02d}.png"
            if icon_file.exists():
                # Map to common names (can be expanded based on actual content)
                if i == 0:
                    icon_map['databricks_sql'] = str(icon_file)
                elif i == 1:
                    icon_map['delta_lake'] = str(icon_file)
                elif i == 2:
                    icon_map['autoloader'] = str(icon_file)
                elif i == 3:
                    icon_map['mlflow'] = str(icon_file)
                elif i == 4:
                    icon_map['unity_catalog'] = str(icon_file)
                elif i == 5:
                    icon_map['mosaic_ai'] = str(icon_file)
                elif i == 6:
                    icon_map['feature_store'] = str(icon_file)
                elif i == 7:
                    icon_map['workflows'] = str(icon_file)
                elif i == 8:
                    icon_map['sql_warehouse'] = str(icon_file)
                elif i == 9:
                    icon_map['lakehouse'] = str(icon_file)
                else:
                    icon_map[f'databricks_icon_{i}'] = str(icon_file)

        # Cloud service logos (slide 26)
        cloud_icons = {
            0: 's3_storage',
            1: 'azure_blob',
            2: 'gcp_storage',
            3: 'kafka',
            4: 'snowflake',
        }
        for i, name in cloud_icons.items():
            icon_file = self.icons_dir / f"template_s026_i{i:02d}.png"
            if icon_file.exists():
                icon_map[name] = str(icon_file)

        # Partner logos (slide 27)
        partner_icons = {
            0: 'tableau',
            1: 'powerbi',
            2: 'looker',
        }
        for i, name in partner_icons.items():
            icon_file = self.icons_dir / f"template_s027_i{i:02d}.png"
            if icon_file.exists():
                icon_map[name] = str(icon_file)

        # Use default Databricks logo for unknown
        default_logo = self.icons_dir / "template_s023_i16.png"
        if default_logo.exists():
            icon_map['default'] = str(default_logo)

        return icon_map

    def get_icon(self, icon_name):
        """Get icon path for given name, or default if not found"""
        return self.icon_mapping.get(icon_name, self.icon_mapping.get('default', ''))

    def _get_graph_attr(self):
        """Get modern graph attributes"""
        return {
            "fontname": "DM Sans",
            "fontsize": "14",
            "bgcolor": "white",
            "pad": "0.5",
            "nodesep": "0.6",
            "ranksep": "1.2",
            "dpi": "300",
        }

    def _get_edge(self, label="", color=None, flow_type="data"):
        """Create modern edge with 1px width"""
        if color is None:
            color_map = {
                'ingest': self.COLORS['light_blue'],
                'process': self.COLORS['medium_blue'],
                'transform': self.COLORS['dark_navy'],
                'serve': self.COLORS['green'],
                'consume': self.COLORS['orange'],
            }
            color = color_map.get(flow_type, self.COLORS['dark_navy'])

        return Edge(
            color=color,
            penwidth="1.0",
            label=label,
            fontname="DM Sans",
            fontsize="10"
        )

    def generate_modern_medallion(self, output_file="modern_medallion_custom_icons.png"):
        """
        Generate medallion architecture using real Databricks icons

        Returns path to generated image
        """
        print(f"\nGenerating Medallion Architecture with custom Databricks icons...")

        with Diagram(
            "Medallion Architecture - Modern Databricks Style",
            filename=output_file.replace('.png', ''),
            show=False,
            direction="LR",
            graph_attr=self._get_graph_attr(),
            outformat="png"
        ):
            # Data Sources
            with Cluster("Data Sources"):
                if self.get_icon('s3_storage'):
                    source1 = Custom("Cloud\nStorage", self.get_icon('s3_storage'))
                if self.get_icon('kafka'):
                    source2 = Custom("Streaming\nKafka", self.get_icon('kafka'))
                source3 = Custom("Database", self.get_icon('default'))

            # Bronze Layer
            with Cluster(
                "Bronze Layer (Raw)",
                graph_attr={"style": "filled", "fillcolor": "#FFF8F0", "color": self.COLORS['bronze']}
            ):
                if self.get_icon('autoloader'):
                    bronze_loader = Custom("AutoLoader", self.get_icon('autoloader'))
                if self.get_icon('delta_lake'):
                    bronze_delta = Custom("Bronze\nDelta Lake", self.get_icon('delta_lake'))

            # Silver Layer
            with Cluster(
                "Silver Layer (Cleansed)",
                graph_attr={"style": "filled", "fillcolor": "#F8F8F8", "color": self.COLORS['silver']}
            ):
                if self.get_icon('delta_lake'):
                    silver_delta = Custom("Silver\nDelta Lake", self.get_icon('delta_lake'))
                if self.get_icon('unity_catalog'):
                    silver_uc = Custom("Unity\nCatalog", self.get_icon('unity_catalog'))

            # Gold Layer
            with Cluster(
                "Gold Layer (Business)",
                graph_attr={"style": "filled", "fillcolor": "#FFFAF0", "color": self.COLORS['gold']}
            ):
                if self.get_icon('delta_lake'):
                    gold_delta = Custom("Gold\nDelta Lake", self.get_icon('delta_lake'))
                if self.get_icon('feature_store'):
                    gold_features = Custom("Feature\nStore", self.get_icon('feature_store'))

            # Consumption
            with Cluster("Analytics & AI"):
                if self.get_icon('databricks_sql'):
                    sql = Custom("Databricks\nSQL", self.get_icon('databricks_sql'))
                if self.get_icon('mosaic_ai'):
                    ai = Custom("Mosaic AI\nGenAI", self.get_icon('mosaic_ai'))

            # Flow
            [source1, source2, source3] >> self._get_edge("Ingest", flow_type='ingest') >> bronze_loader
            bronze_loader >> self._get_edge(flow_type='process') >> bronze_delta
            bronze_delta >> self._get_edge("Cleanse", flow_type='transform') >> silver_delta
            silver_delta >> self._get_edge("Aggregate", flow_type='transform') >> gold_delta
            gold_delta >> self._get_edge("Serve", flow_type='serve') >> sql
            gold_features >> self._get_edge("AI", flow_type='serve') >> ai

        # Resize to max 1000px
        img_path = f"{output_file.replace('.png', '')}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            # Ensure max dimension is 1000px
            width, height = img.size
            if width > 1000 or height > 1000:
                scale = min(1000 / width, 1000 / height)
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                img.save(img_path)
            print(f"✓ Saved: {img_path} ({img.width}x{img.height}px)")
            return img_path
        else:
            print(f"✗ Failed to generate: {img_path}")
            return None


def main():
    """Generate example diagrams with custom Databricks icons"""
    print("=" * 80)
    print("MODERN DATABRICKS DIAGRAMS WITH CUSTOM ICONS")
    print("=" * 80)
    print("\nUsing extracted 112x112 Databricks icons from databricks_assets/")

    gen = ModernDatabricksIconGenerator()

    # Show available icons
    print(f"\nDiscovered {len(gen.icon_mapping)} Databricks icons:")
    for name, path in sorted(gen.icon_mapping.items()):
        print(f"  • {name}: {Path(path).name}")

    # Generate sample diagram
    print("\n" + "=" * 80)
    gen.generate_modern_medallion()

    print("\n" + "=" * 80)
    print("✅ DIAGRAMS GENERATED WITH MODERN DATABRICKS ICONS!")
    print("=" * 80)


if __name__ == "__main__":
    main()
