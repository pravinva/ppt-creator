"""
Proof of Concept: Enterprise-grade Architecture Diagrams using Diagrams Library
Demonstrates high-quality medallion architecture and Databricks solution diagrams
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark
from diagrams.custom import Custom
from diagrams.aws.storage import S3
from diagrams.azure.analytics import Databricks as AzureDatabricks
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack


def generate_medallion_architecture():
    """
    Generate enterprise-grade Medallion Architecture diagram
    Uses professional icons and layout
    """
    graph_attr = {
        "fontsize": "24",
        "bgcolor": "white",
        "pad": "0.5",
        "nodesep": "0.8",
        "ranksep": "1.5"
    }

    with Diagram(
        "Medallion Architecture - Databricks Lakehouse",
        filename="medallion_architecture_poc",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Data Sources
        with Cluster("Data Sources"):
            source1 = Kafka("Streaming\nData")
            source2 = PostgreSQL("Transactional\nDB")
            source3 = S3("File\nStorage")

        # Bronze Layer
        with Cluster("Bronze Layer\n(Raw Data)"):
            bronze_ingest = Storage("Raw\nIngestion")
            bronze_spark = Spark("Schema\nEnforcement")

        # Silver Layer
        with Cluster("Silver Layer\n(Cleaned & Validated)"):
            silver_spark = Spark("Data\nCleansing")
            silver_storage = Storage("Validated\nData")

        # Gold Layer
        with Cluster("Gold Layer\n(Business-Level Aggregated)"):
            gold_spark = Spark("Feature\nEngineering")
            gold_storage = Storage("Analytics-Ready\nTables")

        # Consumption
        with Cluster("Data Consumption"):
            ml = Python("ML Models")
            bi = Rack("BI Dashboards")

        # Connect the flow
        [source1, source2, source3] >> Edge(color="darkblue", style="bold", label="Ingest") >> bronze_ingest >> bronze_spark
        bronze_spark >> Edge(color="darkgreen", style="bold", label="Cleanse") >> silver_spark >> silver_storage
        silver_storage >> Edge(color="orange", style="bold", label="Aggregate") >> gold_spark >> gold_storage
        gold_storage >> Edge(color="purple", style="bold", label="Consume") >> [ml, bi]


def generate_lakehouse_architecture():
    """
    Generate Databricks Lakehouse Architecture diagram
    Shows end-to-end data platform
    """
    graph_attr = {
        "fontsize": "24",
        "bgcolor": "white",
        "pad": "0.5",
        "nodesep": "0.8",
        "ranksep": "1.5"
    }

    with Diagram(
        "Databricks Lakehouse Platform",
        filename="lakehouse_architecture_poc",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Ingestion Layer
        with Cluster("Data Ingestion"):
            kafka_ingest = Kafka("Real-time\nStreaming")
            batch_ingest = Storage("Batch\nFiles")

        # Storage & Processing
        with Cluster("Databricks Lakehouse Platform"):
            with Cluster("Delta Lake Storage"):
                delta = S3("Delta Lake\n(ACID Transactions)")

            with Cluster("Compute"):
                spark_compute = Spark("Spark\nClusters")
                ml_runtime = Python("ML Runtime")

            with Cluster("Data Layers"):
                bronze_layer = Storage("Bronze")
                silver_layer = Storage("Silver")
                gold_layer = Storage("Gold")

                bronze_layer >> silver_layer >> gold_layer

        # Analytics & AI
        with Cluster("Analytics & AI"):
            dashboards = Rack("Dashboards")
            ml_models = Python("ML Models")
            data_apps = PostgreSQL("Data Apps")

        # Connections
        [kafka_ingest, batch_ingest] >> Edge(label="Ingest") >> delta
        delta >> Edge(label="Process") >> spark_compute
        [spark_compute, ml_runtime] >> Edge(label="Transform") >> bronze_layer
        gold_layer >> Edge(label="Serve") >> [dashboards, ml_models, data_apps]


def generate_simple_medallion():
    """
    Generate a cleaner, simpler medallion architecture
    More focused on the three-layer concept
    """
    graph_attr = {
        "fontsize": "28",
        "bgcolor": "white",
        "pad": "0.5",
        "dpi": "300"
    }

    node_attr = {
        "fontsize": "16",
        "width": "2.5",
        "height": "1.5"
    }

    with Diagram(
        "Medallion Architecture",
        filename="medallion_simple_poc",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        node_attr=node_attr,
        outformat="png"
    ):
        # Define layers
        bronze = Storage("Bronze\n━━━━━━━\nRaw Data\nData Ingestion\nSource Systems\nStreaming & Batch")
        silver = Storage("Silver\n━━━━━━━\nCleansed Data\nValidated\nDeduplicated\nConformed")
        gold = Storage("Gold\n━━━━━━━\nBusiness-Level\nAggregated\nFeature Tables\nAnalytics-Ready")

        # Create flow
        bronze >> Edge(color="#CD7F32", style="bold", penwidth="3.0") >> \
        silver >> Edge(color="#C0C0C0", style="bold", penwidth="3.0") >> \
        gold


if __name__ == "__main__":
    print("Generating Medallion Architecture (detailed)...")
    generate_medallion_architecture()
    print("✓ Generated: medallion_architecture_poc.png")

    print("\nGenerating Lakehouse Architecture...")
    generate_lakehouse_architecture()
    print("✓ Generated: lakehouse_architecture_poc.png")

    print("\nGenerating Medallion Architecture (simple)...")
    generate_simple_medallion()
    print("✓ Generated: medallion_simple_poc.png")

    print("\n✅ All diagrams generated successfully!")
    print("These are enterprise-grade diagrams with professional icons.")
