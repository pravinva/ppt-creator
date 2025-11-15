"""
Modern Databricks Architecture Diagram Generator
Based on official 2025 Databricks style guide and templates

Key Features:
- Uses modern Databricks color palette (navy + orange)
- Follows 2025 architecture slide template standards
- Max 1000px dimensions
- DM Sans typography (simulated)
- Clean, minimal design
- Supports AWS, Azure, GCP cloud providers
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.aws.storage import S3
from diagrams.aws.network import VPC as AWSVPC
from diagrams.aws.database import RDS
from diagrams.azure.storage import BlobStorage, DataLakeStorage
from diagrams.azure.network import VirtualNetworks
from diagrams.azure.analytics import Databricks as AzureDatabricks
from diagrams.azure.database import SQLDatabases
from diagrams.gcp.storage import GCS
from diagrams.gcp.network import VPC as GCPVPC
from diagrams.gcp.database import SQL
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL as GenericSQL
from PIL import Image
import io
from typing import Optional, Dict, Any
from pathlib import Path


class ModernDatabricksGenerator:
    """
    Generate Databricks architecture diagrams following 2025 official style guide

    Style Guidelines:
    - Color palette: Navy (#1B3139) + Orange (#FF3621)
    - Max size: 1000px width or height
    - Font: DM Sans (normal weight)
    - Background: Always white (never transparent)
    - Connectors: 1px width
    - Flow: Left-to-right preferred
    - Icons: 112x112 Databricks icons
    """

    # Official Databricks 2025 Color Palette
    COLORS = {
        # Primary colors
        'dark_navy': '#1B3139',      # Primary text and borders
        'medium_blue': '#1B5162',    # Secondary elements
        'light_blue': '#618794',     # Tertiary elements

        # Accent colors
        'orange': '#FF3621',         # Key highlights and CTAs
        'yellow': '#FFAB00',         # Warnings/special attention
        'green': '#00A972',          # Success/data flow
        'red': '#98102A',            # Errors/critical
        'azure_blue': '#0078D4',     # Azure cloud services

        # Neutrals
        'white': '#FFFFFF',          # Background
        'off_white': '#F9F7F4',      # Subtle backgrounds
        'light_gray': '#EFEFEF',     # Disabled states
        'gray': '#D9D9D9',           # Borders and dividers
        'medium_gray': '#B7B7B7',    # Secondary text
        'dark_gray': '#666666',      # Supporting text

        # Medallion architecture colors
        'bronze': '#CD7F32',
        'silver': '#C0C0C0',
        'gold': '#FFD700',
    }

    def __init__(self, cloud_provider: str = "aws", custom_icons_dir: str = "databricks_assets"):
        """
        Initialize modern diagram generator

        Args:
            cloud_provider: Cloud provider ("aws", "azure", or "gcp")
            custom_icons_dir: Directory containing Databricks custom icons
        """
        self.cloud_provider = cloud_provider.lower()
        self.custom_icons_dir = Path(custom_icons_dir)

        # Cloud provider detection keywords
        self.cloud_keywords = {
            'azure': ['azure', 'adls', 'vnet', 'blob', 'synapse'],
            'aws': ['aws', 's3', 'vpc', 'ec2', 'glue', 'kinesis'],
            'gcp': ['gcp', 'google cloud', 'gcs', 'bigquery', 'dataflow']
        }

    def _detect_cloud_provider(self, description: str) -> str:
        """Auto-detect cloud provider from description"""
        if not description:
            return self.cloud_provider

        description_lower = description.lower()

        for provider, keywords in self.cloud_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return provider

        return self.cloud_provider

    def _get_modern_graph_attr(self, max_dimension: int = 1000) -> dict:
        """
        Get graph attributes following modern Databricks style

        Guidelines:
        - Max 1000px width or height
        - White background (never transparent)
        - DPI 300 for high quality
        - Font size 10-16pt range
        """
        return {
            "fontname": "DM Sans",       # Modern Databricks font
            "fontsize": "14",            # Within 10-16pt range
            "bgcolor": "white",          # Always white
            "pad": "0.5",
            "nodesep": "0.6",            # Tighter spacing for modern look
            "ranksep": "1.2",
            "dpi": "300",                # High quality output
        }

    def _get_modern_node_attr(self) -> dict:
        """Get node attributes for modern style"""
        return {
            "fontname": "DM Sans",
            "fontsize": "12",
            "fontcolor": self.COLORS['dark_navy'],  # Near-black for text
            "penwidth": "1.0",           # 1px borders as per guidelines
        }

    def _get_modern_edge(self, label: str = "", color: str = None, flow_type: str = "data") -> Edge:
        """
        Create modern styled edge (1px connectors)

        Args:
            label: Edge label
            color: Color (defaults based on flow type)
            flow_type: Type of flow (data, process, consume)
        """
        if color is None:
            color_map = {
                'ingest': self.COLORS['light_blue'],
                'process': self.COLORS['medium_blue'],
                'transform': self.COLORS['dark_navy'],
                'serve': self.COLORS['green'],
                'consume': self.COLORS['orange'],
                'data': self.COLORS['dark_navy'],
            }
            color = color_map.get(flow_type, self.COLORS['dark_navy'])

        return Edge(
            color=color,
            penwidth="1.0",  # 1px as per guidelines
            label=label,
            fontname="DM Sans",
            fontsize="10",
            fontcolor=self.COLORS['dark_gray']
        )

    def _get_storage_node(self, label: str, cloud: str = None):
        """Get appropriate storage node based on cloud provider"""
        cloud = cloud or self.cloud_provider

        if cloud == 'azure':
            return DataLakeStorage(label)
        elif cloud == 'aws':
            return S3(label)
        elif cloud == 'gcp':
            return GCS(label)
        else:
            return Storage(label)

    def _get_databricks_node(self, label: str):
        """Get Databricks custom icon node"""
        # Try to use custom Databricks icon if available
        icon_path = self.custom_icons_dir / "template_s024_i00.png"  # First Databricks icon
        if icon_path.exists():
            return Custom(label, str(icon_path))
        else:
            # Fallback to Spark icon
            return Spark(label)

    def generate_medallion_architecture(
        self,
        description: str = None,
        include_governance: bool = True
    ) -> Image.Image:
        """
        Generate modern medallion architecture diagram

        Following 2025 Databricks style:
        - Left-to-right flow
        - Navy + orange color scheme
        - Clean, minimal design
        - 1px connectors
        - White background

        Args:
            description: Optional description to customize diagram
            include_governance: Include Unity Catalog governance layer

        Returns:
            PIL Image object
        """
        cloud = self._detect_cloud_provider(description)

        temp_filename = "modern_medallion_arch"

        with Diagram(
            f"Medallion Architecture - Databricks Lakehouse",
            filename=temp_filename,
            show=False,
            direction="LR",  # Left-to-right as per guidelines
            graph_attr=self._get_modern_graph_attr(),
            node_attr=self._get_modern_node_attr(),
            outformat="png"
        ):
            # Data Sources
            with Cluster("Data Sources", graph_attr={"style": "dotted", "color": self.COLORS['medium_gray']}):
                if cloud == 'azure':
                    source1 = BlobStorage("Blob\nStorage")
                    source2 = SQLDatabases("Azure SQL")
                elif cloud == 'aws':
                    source1 = S3("S3 Buckets")
                    source2 = RDS("RDS")
                elif cloud == 'gcp':
                    source1 = GCS("Cloud\nStorage")
                    source2 = SQL("Cloud SQL")
                else:
                    source1 = Storage("Storage")
                    source2 = GenericSQL("Database")

                source3 = Kafka("Streaming\nData")

            # Bronze Layer (Raw Data)
            with Cluster(
                "Bronze Layer\n(Raw Data)",
                graph_attr={
                    "style": "filled",
                    "color": self.COLORS['bronze'],
                    "fillcolor": "#FFF8F0"  # Light bronze background
                }
            ):
                bronze = self._get_storage_node("Bronze\nDelta Lake", cloud)

            # Silver Layer (Cleansed)
            with Cluster(
                "Silver Layer\n(Cleansed & Validated)",
                graph_attr={
                    "style": "filled",
                    "color": self.COLORS['silver'],
                    "fillcolor": "#F8F8F8"  # Light silver background
                }
            ):
                silver = self._get_storage_node("Silver\nDelta Lake", cloud)

            # Gold Layer (Business-Level)
            with Cluster(
                "Gold Layer\n(Business-Level)",
                graph_attr={
                    "style": "filled",
                    "color": self.COLORS['gold'],
                    "fillcolor": "#FFFAF0"  # Light gold background
                }
            ):
                gold = self._get_storage_node("Gold\nDelta Lake", cloud)

            # Consumption Layer
            with Cluster("Data Consumption", graph_attr={"style": "dotted", "color": self.COLORS['medium_gray']}):
                bi = Rack("BI Tools\n(Tableau, Power BI)")
                ml = Python("ML Models\n(MLflow)")

            # Modern flow with 1px edges
            [source1, source2, source3] >> self._get_modern_edge("Ingest", flow_type='ingest') >> bronze
            bronze >> self._get_modern_edge("Cleanse & Validate", flow_type='process') >> silver
            silver >> self._get_modern_edge("Aggregate & Transform", flow_type='transform') >> gold
            gold >> self._get_modern_edge("Serve", flow_type='serve') >> [bi, ml]

        # Load and return the generated image
        img_path = f"{temp_filename}.png"
        img = Image.open(img_path)

        # Ensure max dimension is 1000px (following guidelines)
        img = self._resize_to_max_dimension(img, 1000)

        return img

    def generate_lakehouse_architecture(
        self,
        description: str = None,
        show_unity_catalog: bool = True
    ) -> Image.Image:
        """
        Generate modern Databricks lakehouse architecture

        Follows swim lane pattern:
        Source → Ingest → Transform → Query/Process → Serve → Analysis

        Args:
            description: Description for customization
            show_unity_catalog: Show Unity Catalog governance

        Returns:
            PIL Image object
        """
        cloud = self._detect_cloud_provider(description)

        temp_filename = "modern_lakehouse_arch"

        with Diagram(
            f"Databricks Lakehouse Architecture",
            filename=temp_filename,
            show=False,
            direction="LR",  # Left-to-right flow
            graph_attr=self._get_modern_graph_attr(),
            node_attr=self._get_modern_node_attr(),
            outformat="png"
        ):
            # Source Layer
            with Cluster("Source"):
                streaming = Kafka("Streaming")
                batch = Storage("Batch Files")
                databases = GenericSQL("Databases")

            # Ingest Layer
            with Cluster("Ingest"):
                autoloader = Spark("AutoLoader")

            # Transform Layer (Medallion)
            with Cluster("Transform\n(Medallion)"):
                with Cluster(""):
                    bronze = Storage("Bronze")
                    silver = Storage("Silver")
                    gold = Storage("Gold")
                    bronze >> silver >> gold

            # Storage Layer
            with Cluster("Storage"):
                delta_lake = self._get_storage_node("Delta Lake", cloud)

            # Query/Process Layer
            with Cluster("Query/Process"):
                sql_warehouse = Spark("SQL\nWarehouse")
                ml_runtime = Python("ML\nRuntime")

            # Serve Layer
            with Cluster("Serve"):
                apis = Rack("REST APIs")
                delta_sharing = Storage("Delta\nSharing")

            # Analysis Layer
            with Cluster("Analysis"):
                bi_tools = Rack("BI Tools")
                notebooks = Python("Notebooks")

            # Connections (modern 1px edges)
            [streaming, batch, databases] >> self._get_modern_edge(flow_type='ingest') >> autoloader
            autoloader >> self._get_modern_edge(flow_type='process') >> bronze
            gold >> self._get_modern_edge(flow_type='transform') >> delta_lake
            delta_lake >> self._get_modern_edge(flow_type='process') >> sql_warehouse
            delta_lake >> self._get_modern_edge(flow_type='process') >> ml_runtime
            sql_warehouse >> self._get_modern_edge(flow_type='serve') >> apis
            ml_runtime >> self._get_modern_edge(flow_type='serve') >> delta_sharing
            apis >> self._get_modern_edge(flow_type='consume') >> bi_tools
            delta_sharing >> self._get_modern_edge(flow_type='consume') >> notebooks

        # Load and resize
        img_path = f"{temp_filename}.png"
        img = Image.open(img_path)
        img = self._resize_to_max_dimension(img, 1000)

        return img

    def generate_streaming_architecture(self, description: str = None) -> Image.Image:
        """Generate real-time streaming analytics architecture"""
        cloud = self._detect_cloud_provider(description)

        temp_filename = "modern_streaming_arch"

        with Diagram(
            "Real-Time Streaming Analytics",
            filename=temp_filename,
            show=False,
            direction="LR",
            graph_attr=self._get_modern_graph_attr(),
            node_attr=self._get_modern_node_attr(),
            outformat="png"
        ):
            # Streaming sources
            with Cluster("Streaming Sources"):
                kafka = Kafka("Kafka")
                iot = Storage("IoT Devices")

            # Ingestion
            with Cluster("Stream Processing"):
                structured_streaming = Spark("Structured\nStreaming")

            # Storage
            with Cluster("Delta Lake"):
                delta = self._get_storage_node("Delta\nTables", cloud)

            # Analytics
            with Cluster("Analytics"):
                sql = Spark("SQL\nAnalytics")
                dashboard = Rack("Real-time\nDashboards")

            # Flow
            [kafka, iot] >> self._get_modern_edge("Stream", flow_type='ingest') >> structured_streaming
            structured_streaming >> self._get_modern_edge("Write", flow_type='process') >> delta
            delta >> self._get_modern_edge("Query", flow_type='serve') >> sql
            sql >> self._get_modern_edge("Visualize", flow_type='consume') >> dashboard

        img_path = f"{temp_filename}.png"
        img = Image.open(img_path)
        img = self._resize_to_max_dimension(img, 1000)

        return img

    def _resize_to_max_dimension(self, img: Image.Image, max_dim: int) -> Image.Image:
        """
        Resize image to ensure max dimension is not exceeded
        Maintains aspect ratio

        Following guideline: Max 1000px width or height
        """
        width, height = img.size

        if width <= max_dim and height <= max_dim:
            return img

        # Calculate scaling factor
        scale = min(max_dim / width, max_dim / height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def save_diagram(self, image: Image.Image, filepath: str):
        """Save diagram to file"""
        # Ensure white background (never transparent)
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, 'white')
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[3])  # Alpha channel
            else:
                background.paste(image, mask=image.split()[1])
            image = background

        image.save(filepath, 'PNG')

    def get_image_bytes(self, image: Image.Image) -> bytes:
        """Convert image to bytes for embedding in PowerPoint"""
        # Ensure white background
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, 'white')
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[3])
            else:
                background.paste(image, mask=image.split()[1])
            image = background

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr


if __name__ == "__main__":
    print("=" * 80)
    print("MODERN DATABRICKS DIAGRAM GENERATOR (2025 Style)")
    print("=" * 80)
    print("\nFollowing official Databricks style guide:")
    print("  ✓ Navy + Orange color scheme")
    print("  ✓ Max 1000px dimensions")
    print("  ✓ DM Sans typography")
    print("  ✓ 1px connectors")
    print("  ✓ White background")
    print("  ✓ Clean, minimal design\n")

    # Test AWS
    print("1. Generating AWS Medallion Architecture...")
    gen_aws = ModernDatabricksGenerator(cloud_provider="aws")
    img_aws = gen_aws.generate_medallion_architecture("AWS S3 based medallion architecture")
    gen_aws.save_diagram(img_aws, "modern_aws_medallion.png")
    print(f"   ✓ Saved: modern_aws_medallion.png ({img_aws.width}x{img_aws.height}px)\n")

    # Test Azure
    print("2. Generating Azure Lakehouse Architecture...")
    gen_azure = ModernDatabricksGenerator(cloud_provider="azure")
    img_azure = gen_azure.generate_lakehouse_architecture("Azure ADLS Gen2 lakehouse")
    gen_azure.save_diagram(img_azure, "modern_azure_lakehouse.png")
    print(f"   ✓ Saved: modern_azure_lakehouse.png ({img_azure.width}x{img_azure.height}px)\n")

    # Test GCP Streaming
    print("3. Generating GCP Streaming Architecture...")
    gen_gcp = ModernDatabricksGenerator(cloud_provider="gcp")
    img_gcp = gen_gcp.generate_streaming_architecture("GCP Pub/Sub streaming")
    gen_gcp.save_diagram(img_gcp, "modern_gcp_streaming.png")
    print(f"   ✓ Saved: modern_gcp_streaming.png ({img_gcp.width}x{img_gcp.height}px)\n")

    print("=" * 80)
    print("✅ ALL MODERN DIAGRAMS GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print("\nKey improvements from old style:")
    print("  • Modern color palette (navy #1B3139 + orange #FF3621)")
    print("  • Proper sizing (max 1000px)")
    print("  • Clean typography (DM Sans)")
    print("  • Professional spacing and alignment")
    print("  • Cloud-aware icons (AWS/Azure/GCP)")
    print("  • Follows 2025 Databricks guidelines")
