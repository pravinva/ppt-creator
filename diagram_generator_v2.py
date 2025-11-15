"""
Enterprise Diagram Generator for Databricks Architecture Diagrams
Uses Diagrams library with professional icons and cloud-aware support
Supports Azure, AWS, and GCP with appropriate cloud provider icons
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


class DiagramGenerator:
    """Generate cloud-aware Databricks architecture diagrams with professional icons"""

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

    def __init__(self, width: int = 1280, height: int = 720, cloud_provider: str = "aws"):
        """
        Initialize diagram generator

        Args:
            width: Not used in Diagrams library (kept for backward compatibility)
            height: Not used in Diagrams library (kept for backward compatibility)
            cloud_provider: Cloud provider ("aws", "azure", or "gcp")
        """
        self.width = width
        self.height = height
        self.cloud_provider = cloud_provider.lower()
        self.custom_icons_dir = Path("custom_icons")

        # Detect cloud provider from common keywords
        self.cloud_keywords = {
            'azure': ['azure', 'adls', 'vnet', 'blob storage'],
            'aws': ['aws', 's3', 'vpc', 'ec2'],
            'gcp': ['gcp', 'google cloud', 'gcs', 'bigquery']
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
        icon_path = self.custom_icons_dir / "databricks_logo.png"
        if icon_path.exists():
            return Custom(label, str(icon_path))
        else:
            # Fallback to Spark icon if custom icon not available
            return Spark(label)

    def _get_delta_lake_node(self, label: str, cloud: str = None):
        """Get Delta Lake storage node"""
        cloud = cloud or self.cloud_provider
        return self._get_storage_node(f"{label}\n(Delta Lake)", cloud)

    def generate_medallion_architecture(self, description: str = None) -> Image.Image:
        """
        Generate enterprise-grade medallion architecture diagram
        Auto-detects cloud provider from description

        Args:
            description: Optional description to customize and detect cloud provider

        Returns:
            PIL Image object
        """
        cloud = self._detect_cloud_provider(description)

        graph_attr = {
            "fontsize": "24",
            "bgcolor": "white",
            "pad": "0.5",
            "nodesep": "0.8",
            "ranksep": "1.5",
            "dpi": "300"
        }

        # Create temp filename
        temp_filename = "temp_medallion_arch"

        with Diagram(
            f"Medallion Architecture - Databricks on {cloud.upper()}",
            filename=temp_filename,
            show=False,
            direction="LR",
            graph_attr=graph_attr,
            outformat="png"
        ):
            # Data Sources (cloud-specific)
            with Cluster("Data Sources"):
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

            # Bronze Layer
            with Cluster("Bronze Layer\n(Raw Data)"):
                bronze_storage = self._get_delta_lake_node("Bronze\nRaw Data", cloud)
                bronze_process = Spark("Schema\nEnforcement")

            # Silver Layer
            with Cluster("Silver Layer\n(Cleaned & Validated)"):
                silver_storage = self._get_delta_lake_node("Silver\nCleansed Data", cloud)
                silver_process = Spark("Data\nCleansing")

            # Gold Layer
            with Cluster("Gold Layer\n(Business-Level)"):
                gold_storage = self._get_delta_lake_node("Gold\nAnalytics-Ready", cloud)
                gold_process = Spark("Feature\nEngineering")

            # Consumption
            with Cluster("Data Consumption"):
                ml = Python("ML Models")
                bi = Rack("BI\nDashboards")

            # Flow
            [source1, source2, source3] >> Edge(color="#CD7F32", style="bold", label="Ingest") >> bronze_storage >> bronze_process
            bronze_process >> Edge(color="#C0C0C0", style="bold", label="Cleanse") >> silver_process >> silver_storage
            silver_storage >> Edge(color="#FFD700", style="bold", label="Aggregate") >> gold_process >> gold_storage
            gold_storage >> Edge(color="#FF3621", style="bold", label="Consume") >> [ml, bi]

        # Load and return the generated image
        img_path = f"{temp_filename}.png"
        img = Image.open(img_path)
        return img

    def generate_architecture_diagram(self, description: str = None) -> Image.Image:
        """
        Generate cloud-aware Databricks lakehouse architecture diagram

        Args:
            description: Description to guide and detect cloud provider

        Returns:
            PIL Image object
        """
        cloud = self._detect_cloud_provider(description)

        graph_attr = {
            "fontsize": "24",
            "bgcolor": "white",
            "pad": "0.5",
            "dpi": "300"
        }

        temp_filename = "temp_lakehouse_arch"

        with Diagram(
            f"Databricks Lakehouse on {cloud.upper()}",
            filename=temp_filename,
            show=False,
            direction="TB",
            graph_attr=graph_attr,
            outformat="png"
        ):
            # Ingestion
            with Cluster("Data Ingestion"):
                streaming = Kafka("Real-time\nStreaming")
                batch = Storage("Batch\nFiles")

            # Cloud Network
            if cloud == 'azure':
                with Cluster("Azure VNet"):
                    network = VirtualNetworks("VNet")
            elif cloud == 'aws':
                with Cluster("AWS VPC"):
                    network = AWSVPC("VPC")
            elif cloud == 'gcp':
                with Cluster("GCP VPC"):
                    network = GCPVPC("VPC")
            else:
                network = None

            # Databricks Platform
            with Cluster("Databricks Lakehouse Platform"):
                # Storage
                delta_storage = self._get_delta_lake_node("Delta Lake\nACID Storage", cloud)

                # Compute
                with Cluster("Compute Clusters"):
                    spark_cluster = Spark("Spark\nClusters")
                    ml_runtime = Python("ML\nRuntime")

                # Medallion layers
                with Cluster("Data Layers"):
                    bronze = Storage("Bronze")
                    silver = Storage("Silver")
                    gold = Storage("Gold")

                    bronze >> silver >> gold

            # Analytics
            with Cluster("Analytics & AI"):
                dashboards = Rack("BI\nDashboards")
                ml_models = Python("ML\nModels")
                apps = GenericSQL("Data\nApps")

            # Connections
            [streaming, batch] >> Edge(label="Ingest") >> delta_storage
            delta_storage >> Edge(label="Process") >> spark_cluster
            [spark_cluster, ml_runtime] >> Edge(label="Transform") >> bronze
            gold >> Edge(label="Serve") >> [dashboards, ml_models, apps]

        # Load and return
        img_path = f"{temp_filename}.png"
        img = Image.open(img_path)
        return img

    def save_diagram(self, image: Image.Image, filepath: str):
        """Save diagram to file (backward compatible)"""
        image.save(filepath, 'PNG')

    def get_image_bytes(self, image: Image.Image) -> bytes:
        """Convert image to bytes for embedding in PowerPoint (backward compatible)"""
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr


if __name__ == "__main__":
    print("Testing cloud-aware diagram generation...\n")

    # Test AWS
    print("1. Generating AWS Databricks architecture...")
    gen_aws = DiagramGenerator(cloud_provider="aws")
    img_aws = gen_aws.generate_medallion_architecture("Databricks on AWS with S3 and VPC")
    gen_aws.save_diagram(img_aws, "test_aws_medallion.png")
    print("   ✓ Saved: test_aws_medallion.png\n")

    # Test Azure
    print("2. Generating Azure Databricks architecture...")
    gen_azure = DiagramGenerator(cloud_provider="azure")
    img_azure = gen_azure.generate_medallion_architecture("Databricks on Azure with ADLS and VNet")
    gen_azure.save_diagram(img_azure, "test_azure_medallion.png")
    print("   ✓ Saved: test_azure_medallion.png\n")

    # Test GCP
    print("3. Generating GCP Databricks architecture...")
    gen_gcp = DiagramGenerator(cloud_provider="gcp")
    img_gcp = gen_gcp.generate_architecture_diagram("Databricks on Google Cloud Platform")
    gen_gcp.save_diagram(img_gcp, "test_gcp_lakehouse.png")
    print("   ✓ Saved: test_gcp_lakehouse.png\n")

    print("✅ All cloud-aware diagrams generated successfully!")
    print("\nThe diagrams automatically use the appropriate cloud provider icons:")
    print("  - AWS: S3, VPC, RDS")
    print("  - Azure: Blob Storage, VNet, Azure SQL")
    print("  - GCP: GCS, VPC, Cloud SQL")
