"""
POC: Databricks Workspace Migration - Environment to Domain-Based Catalogs
Single Unity Catalog Metastore Architecture with Phased Migration

Demonstrates:
1. Cloud-aware architecture diagrams (before/after migration)
2. Project timeline with phased approach
3. CPM analysis showing critical path
"""
from diagram_generator import DiagramGenerator
from gantt_generator import GanttGenerator
from pyCritical.src.cpm_pert import critical_path_method
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.analytics import Spark
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL
from diagrams.aws.storage import S3
from diagrams.azure.storage import DataLakeStorage
from diagrams.gcp.storage import GCS
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def generate_migration_architecture(cloud_provider="azure"):
    """
    Generate before/after architecture showing single metastore approach
    """
    print(f"\n1. Generating Migration Architecture Diagram ({cloud_provider.upper()})...")

    # Detect storage based on cloud
    if cloud_provider == "azure":
        storage_node = DataLakeStorage
        storage_label = "ADLS Gen2"
    elif cloud_provider == "aws":
        storage_node = S3
        storage_label = "S3"
    elif cloud_provider == "gcp":
        storage_node = GCS
        storage_label = "GCS"
    else:
        storage_node = Storage
        storage_label = "Storage"

    graph_attr = {
        "fontsize": "20",
        "bgcolor": "white",
        "pad": "0.5",
        "dpi": "300",
        "rankdir": "TB"
    }

    # Create comprehensive migration diagram
    with Diagram(
        f"Unity Catalog Migration - Single Metastore Architecture ({cloud_provider.upper()})",
        filename="migration_architecture",
        show=False,
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Single Unity Catalog Metastore (top)
        with Cluster("Unity Catalog Metastore (Single)"):
            metastore = Storage("Unity Catalog\nMetastore")

            with Cluster("Domain-Based Catalogs"):
                customer_cat = SQL("Customer\nCatalog")
                finance_cat = SQL("Finance\nCatalog")
                operations_cat = SQL("Operations\nCatalog")

            with Cluster("Compatibility Views"):
                compat_views = Python("Compatibility\nViews Layer")

        # LZ1 Workspace (Legacy)
        with Cluster("LZ1 Workspace (Legacy)\nEnvironment-Based"):
            lz1_dev = Rack("Dev\nEnvironment")
            lz1_uat = Rack("UAT\nEnvironment")
            lz1_prod = Rack("Prod\nEnvironment")

            with Cluster("Legacy Jobs"):
                lz1_jobs = Spark("Legacy\nJobs")

        # LZ2 Workspace (New)
        with Cluster("LZ2 Workspace (New)\nDomain-Based"):
            lz2_dev = Rack("Dev\nEnvironment")
            lz2_uat = Rack("UAT\nEnvironment")
            lz2_prod = Rack("Prod\nEnvironment")

            with Cluster("Migrated Jobs"):
                lz2_jobs = Spark("Domain\nJobs")

        # Data Storage
        with Cluster(f"Data Layer ({storage_label})"):
            data_storage = storage_node("Delta Lake\nStorage")

        # BI Tools
        with Cluster("BI Tools"):
            bi_tools = Rack("Power BI\nTableau")

        # Connections
        # Metastore to catalogs
        metastore >> [customer_cat, finance_cat, operations_cat]

        # Catalogs to compatibility views
        [customer_cat, finance_cat, operations_cat] >> compat_views

        # LZ1 workspace uses compatibility views (gradual migration)
        lz1_dev >> Edge(label="Uses", color="orange", style="dashed") >> compat_views
        lz1_uat >> Edge(color="orange", style="dashed") >> compat_views
        lz1_prod >> Edge(color="orange", style="dashed") >> compat_views
        lz1_jobs >> Edge(label="Reads via\nCompat Views", color="orange") >> compat_views

        # LZ2 workspace uses domain catalogs directly
        lz2_dev >> Edge(label="Direct Access", color="green", style="bold") >> customer_cat
        lz2_uat >> Edge(color="green", style="bold") >> finance_cat
        lz2_prod >> Edge(color="green", style="bold") >> operations_cat
        lz2_jobs >> Edge(label="Reads from\nDomain Catalogs", color="green") >> customer_cat
        lz2_jobs >> Edge(color="green") >> finance_cat
        lz2_jobs >> Edge(color="green") >> operations_cat

        # Both write to data storage
        customer_cat >> Edge(label="Stores") >> data_storage
        finance_cat >> Edge(label="") >> data_storage
        operations_cat >> Edge(label="") >> data_storage

        # BI Tools access both (gradual migration)
        bi_tools >> Edge(label="Migrating", color="blue") >> compat_views
        bi_tools >> Edge(label="New Queries", color="green") >> customer_cat

    print("   ✅ Saved: migration_architecture.png")
    print("   • Single Unity Catalog metastore")
    print("   • Domain-based catalogs (Customer, Finance, Operations)")
    print("   • Compatibility views for gradual migration")
    print("   • LZ1 → LZ2 workspace migration path")

    return Image.open("migration_architecture.png")


def generate_migration_timeline():
    """
    Generate Gantt chart for phased migration approach
    """
    print("\n2. Generating Migration Timeline (Gantt Chart)...")

    tasks = [
        {'name': 'Phase 0: Planning & Design', 'start': '2024-01-01', 'duration': 30, 'phase': 'planning'},
        {'name': 'Phase 1: Create LZ2 Workspaces', 'start': '2024-02-01', 'duration': 15, 'phase': 'development'},
        {'name': 'Phase 1: Bind to Existing Metastore', 'start': '2024-02-10', 'duration': 10, 'phase': 'development'},
        {'name': 'Phase 2: Deploy Compatibility Views', 'start': '2024-02-20', 'duration': 20, 'phase': 'silver'},
        {'name': 'Phase 3a: Migrate Customer Domain', 'start': '2024-03-10', 'duration': 30, 'phase': 'bronze'},
        {'name': 'Phase 3b: Migrate Finance Domain', 'start': '2024-04-05', 'duration': 30, 'phase': 'silver'},
        {'name': 'Phase 3c: Migrate Operations Domain', 'start': '2024-05-01', 'duration': 30, 'phase': 'gold'},
        {'name': 'Phase 4: BI Tool Migration (Gradual)', 'start': '2024-03-20', 'duration': 75, 'phase': 'testing'},
        {'name': 'Phase 4: Validate Reports', 'start': '2024-05-15', 'duration': 30, 'phase': 'testing'},
        {'name': 'Phase 5: Decommission LZ1 Prep', 'start': '2024-06-01', 'duration': 20, 'phase': 'deployment'},
        {'name': 'Phase 5: Final LZ1 Shutdown', 'start': '2024-06-20', 'duration': 10, 'phase': 'deployment'},
        {'name': 'Post-Migration: Monitoring (30d)', 'start': '2024-06-30', 'duration': 30, 'phase': 'maintenance'},
    ]

    generator = GanttGenerator(figsize=(18, 10), dpi=300)
    img = generator.generate_project_timeline(
        tasks,
        title="Unity Catalog Migration - Phased Approach (Single Metastore)"
    )

    generator.save_chart(img, "migration_timeline.png")

    print("   ✅ Saved: migration_timeline.png")
    print("   • 6-month phased migration")
    print("   • Domain-by-domain migration (Customer → Finance → Operations)")
    print("   • Parallel BI tool migration")
    print("   • No big bang cutover required")

    return img


def generate_migration_cpm():
    """
    Generate CPM analysis showing critical path for migration
    """
    print("\n3. Generating CPM Analysis (Critical Path)...")

    # Define tasks with dependencies
    tasks_cpm = [
        ['Planning', [], 30],
        ['Create LZ2', ['Planning'], 15],
        ['Bind Metastore', ['Create LZ2'], 10],
        ['Deploy Compat Views', ['Bind Metastore'], 20],
        ['Migrate Customer', ['Deploy Compat Views'], 30],
        ['Migrate Finance', ['Migrate Customer'], 30],
        ['Migrate Operations', ['Migrate Finance'], 30],
        ['BI Migration', ['Deploy Compat Views'], 75],  # Can start early, runs parallel
        ['Validate Reports', ['BI Migration', 'Migrate Operations'], 30],
        ['Decommission Prep', ['Validate Reports'], 20],
        ['LZ1 Shutdown', ['Decommission Prep'], 10],
        ['Monitoring', ['LZ1 Shutdown'], 30],
    ]

    # Run CPM analysis
    result = critical_path_method(dataset=tasks_cpm)

    print("\n   📊 CPM Analysis Results:")
    print("   " + "=" * 60)
    print(result.to_string().replace('\n', '\n   '))

    # Identify critical path
    critical_tasks = result[result['Slack'] == 0]
    print("\n   🎯 CRITICAL PATH:")
    for task in critical_tasks.index:
        print(f"      → {task}")

    total_duration = result['LF'].max()
    print(f"\n   📅 Total Project Duration: {total_duration:.0f} days (~{total_duration/30:.1f} months)")

    # Calculate slack for non-critical tasks
    non_critical = result[result['Slack'] > 0]
    if len(non_critical) > 0:
        print(f"\n   ⏰ Tasks with Schedule Flexibility:")
        for task in non_critical.index:
            slack = non_critical.loc[task, 'Slack']
            print(f"      • {task}: {slack:.0f} days slack")

    # Generate Gantt with critical path
    from pyCritical.src.cpm_pert import gantt_chart
    fig = plt.figure(figsize=(18, 12), dpi=300)
    gantt_chart(dataset=tasks_cpm, dates=result, size_x=18, size_y=12)

    # Add title and annotations
    plt.suptitle(
        "Unity Catalog Migration - Critical Path Analysis\n"
        "Single Metastore Strategy with Compatibility Views",
        fontsize=16, fontweight='bold', y=0.98
    )

    plt.savefig('migration_cpm.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("\n   ✅ Saved: migration_cpm.png")
    print("   • Critical path highlighted in RED")
    print("   • BI Migration can run in parallel (has slack)")
    print("   • Total duration optimized via phased approach")

    return Image.open('migration_cpm.png')


def generate_benefits_comparison():
    """
    Generate visual comparison: Single vs Dual Metastore
    """
    print("\n4. Generating Benefits Comparison Diagram...")

    graph_attr = {
        "fontsize": "18",
        "bgcolor": "white",
        "pad": "0.5",
        "dpi": "300"
    }

    with Diagram(
        "Single vs Dual Metastore Comparison",
        filename="metastore_comparison",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Left side: DUAL metastore (NOT recommended)
        with Cluster("❌ DUAL Metastore (Not Recommended)"):
            with Cluster("Metastore 1 (LZ1)"):
                ms1 = Storage("Legacy\nMetastore")

            with Cluster("Metastore 2 (LZ2)"):
                ms2 = Storage("New\nMetastore")

            with Cluster("Migration Challenges"):
                bigbang = Rack("Big Bang\nCutover")
                overhead = Rack("Operational\nOverhead")
                norollback = Rack("No Easy\nRollback")

        # Right side: SINGLE metastore (RECOMMENDED)
        with Cluster("✅ SINGLE Metastore (Recommended)"):
            with Cluster("Unity Catalog"):
                single_ms = Storage("Single\nMetastore")

            with Cluster("Domain Catalogs"):
                domains = SQL("Customer\nFinance\nOperations")

            with Cluster("Compatibility Layer"):
                compat = Python("Compat\nViews")

            with Cluster("Benefits"):
                gradual = Rack("Gradual\nMigration")
                decoupled = Rack("Data ↔︎ Infra\nDecoupled")
                rollback = Rack("Instant\nRollback")

        # Show problems with dual
        ms1 >> Edge(color="red", style="bold") >> bigbang
        ms2 >> Edge(color="red", style="bold") >> overhead
        ms1 >> Edge(color="red") >> norollback
        ms2 >> Edge(color="red") >> norollback

        # Show benefits of single
        single_ms >> Edge(color="green") >> domains
        domains >> compat
        compat >> Edge(color="green", style="bold") >> gradual
        compat >> Edge(color="green", style="bold") >> decoupled
        compat >> Edge(color="green", style="bold") >> rollback

    print("   ✅ Saved: metastore_comparison.png")
    print("   • Clear visual: Single vs Dual metastore")
    print("   • Highlights benefits: gradual migration, rollback, decoupling")
    print("   • Shows risks: big bang, overhead, no rollback")

    return Image.open("metastore_comparison.png")


def main():
    """
    Generate complete POC for workspace migration
    """
    print("=" * 70)
    print("Unity Catalog Workspace Migration POC")
    print("Environment-Based → Domain-Based Catalogs")
    print("Single Metastore Strategy with Phased Migration")
    print("=" * 70)

    # Allow cloud provider selection
    cloud = "azure"  # Change to "aws" or "gcp" as needed

    # Generate all diagrams
    arch_img = generate_migration_architecture(cloud_provider=cloud)
    timeline_img = generate_migration_timeline()
    cpm_img = generate_migration_cpm()
    comparison_img = generate_benefits_comparison()

    print("\n" + "=" * 70)
    print("✅ POC GENERATION COMPLETE!")
    print("=" * 70)

    print("\nGenerated Diagrams:")
    print("  1. migration_architecture.png")
    print("     • Single Unity Catalog metastore")
    print("     • LZ1 → LZ2 workspace migration")
    print("     • Compatibility views for gradual migration")
    print("     • Domain-based catalogs (Customer, Finance, Operations)")

    print("\n  2. migration_timeline.png")
    print("     • 6-month phased approach")
    print("     • Domain-by-domain migration")
    print("     • Parallel BI tool migration")
    print("     • Color-coded phases")

    print("\n  3. migration_cpm.png")
    print("     • Critical path analysis")
    print("     • ~6 months total duration")
    print("     • Identifies schedule flexibility")
    print("     • RED = critical, BLUE = has slack")

    print("\n  4. metastore_comparison.png")
    print("     • Single vs Dual metastore comparison")
    print("     • Visual benefits breakdown")
    print("     • Risk mitigation highlights")

    print("\n" + "=" * 70)
    print("KEY RECOMMENDATIONS DEMONSTRATED:")
    print("=" * 70)
    print("✓ Single Unity Catalog metastore (NOT dual)")
    print("✓ Compatibility views enable gradual migration")
    print("✓ Domain-by-domain migration reduces risk")
    print("✓ Instant rollback capability via views")
    print("✓ Data decoupled from infrastructure")
    print("✓ No 'big bang' cutover required")
    print("✓ Independent migration timelines per domain")
    print("✓ BI tools migrate gradually without coordination overhead")

    print("\n" + "=" * 70)
    print("MIGRATION ROADMAP PHASES:")
    print("=" * 70)
    print("Phase 0: Planning & Design (30 days)")
    print("Phase 1: Create LZ2 workspaces + bind to metastore (25 days)")
    print("Phase 2: Deploy compatibility views (20 days)")
    print("Phase 3: Migrate domains one-by-one (90 days)")
    print("         • Customer domain first")
    print("         • Finance domain second")
    print("         • Operations domain third")
    print("Phase 4: Gradual BI tool migration (parallel, 75 days)")
    print("Phase 5: Decommission LZ1 (30 days)")
    print("Post: Monitoring period (30 days)")
    print("\n💡 Total: ~6 months with controlled, reversible migration")


if __name__ == "__main__":
    main()
