"""
Generic Agentic AI Architecture Generator
Works for ANY company/use case based on prompts

Uses modern Databricks icons from databricks_assets/
Follows 2025 Databricks style guide
"""
from diagram_generator_with_custom_icons import ModernDatabricksIconGenerator
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from PIL import Image
import os


class AgenticAIGenerator:
    """
    Generic Agentic AI architecture generator
    Works for any company based on prompts
    """

    def __init__(self):
        """Initialize with modern Databricks icon support"""
        self.icon_gen = ModernDatabricksIconGenerator()

    def generate_journey_diagram(
        self,
        company_name: str,
        phase_descriptions: dict,
        output_file: str = "agentic_journey.png"
    ):
        """
        Generate 4-phase agentic AI journey diagram

        Args:
            company_name: Company name (e.g., "Energy Australia", "Retail Bank")
            phase_descriptions: Dict with phase names and descriptions
            output_file: Output filename

        Example:
            phase_descriptions = {
                "Phase 1": {
                    "title": "Traditional Analytics",
                    "timeline": "Current State",
                    "color": "#666666",
                    "components": ["Historical Data", "BI Reports", "Basic ML"]
                },
                ...
            }
        """
        print(f"\n📊 Generating Agentic AI Journey for {company_name}...")

        with Diagram(
            f"{company_name} - Agentic AI Journey",
            filename=output_file.replace('.png', ''),
            show=False,
            direction="LR",
            graph_attr=self.icon_gen._get_graph_attr(),
            outformat="png"
        ):
            # Dynamically create phases based on input
            for phase_name, phase_info in phase_descriptions.items():
                with Cluster(
                    f"{phase_name}: {phase_info['title']}\n({phase_info['timeline']})",
                    graph_attr={
                        "style": "filled",
                        "color": phase_info.get('color', '#1B3139'),
                        "fillcolor": phase_info.get('fillcolor', '#F5F5F5')
                    }
                ):
                    # Create nodes for each component
                    for component in phase_info['components']:
                        # Try to use Databricks icon if available
                        icon_key = component.lower().replace(' ', '_').replace('/', '_')
                        icon_path = self.icon_gen.get_icon(icon_key)
                        if icon_path:
                            Custom(component, icon_path)
                        else:
                            Custom(component, self.icon_gen.get_icon('default'))

        # Resize and save
        img_path = f"{output_file.replace('.png', '')}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > 1000 or height > 1000:
                scale = min(1000 / width, 1000 / height)
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                img.save(img_path)
            print(f"   ✓ Saved: {img_path} ({img.width}x{img.height}px)")
            return img_path

    def generate_full_architecture(
        self,
        company_name: str,
        architecture_config: dict,
        output_file: str = "agentic_architecture.png"
    ):
        """
        Generate complete agentic AI platform architecture

        Args:
            company_name: Company name
            architecture_config: Configuration with layers and components
            output_file: Output filename

        Example:
            architecture_config = {
                "data_sources": [
                    {"name": "Smart Meters", "icon": "iot"},
                    {"name": "CRM", "icon": "database"}
                ],
                "platform_components": [...],
                "ai_agents": [...],
                "applications": [...]
            }
        """
        print(f"\n🏗️  Generating Full Architecture for {company_name}...")

        with Diagram(
            f"{company_name} - Agentic AI Platform",
            filename=output_file.replace('.png', ''),
            show=False,
            direction="LR",
            graph_attr=self.icon_gen._get_graph_attr(),
            outformat="png"
        ):
            # Data Sources
            sources = []
            if 'data_sources' in architecture_config:
                with Cluster("Data Sources"):
                    for source in architecture_config['data_sources']:
                        icon = self.icon_gen.get_icon(source.get('icon', 'default'))
                        sources.append(Custom(source['name'], icon))

            # Data Platform
            platform_nodes = {}
            if 'platform_components' in architecture_config:
                with Cluster("Databricks Lakehouse Platform"):
                    for component in architecture_config['platform_components']:
                        icon = self.icon_gen.get_icon(component.get('icon', 'default'))
                        platform_nodes[component['name']] = Custom(component['name'], icon)

            # AI Agents
            agents = []
            if 'ai_agents' in architecture_config:
                with Cluster("AI Agents (Autonomous)"):
                    for agent in architecture_config['ai_agents']:
                        icon = self.icon_gen.get_icon(agent.get('icon', 'mosaic_ai'))
                        agents.append(Custom(agent['name'], icon))

            # Applications
            apps = []
            if 'applications' in architecture_config:
                with Cluster("Applications"):
                    for app in architecture_config['applications']:
                        icon = self.icon_gen.get_icon(app.get('icon', 'default'))
                        apps.append(Custom(app['name'], icon))

            # Connections (can be customized)
            if sources and platform_nodes:
                for source in sources:
                    if 'AutoLoader' in platform_nodes:
                        source >> self.icon_gen._get_edge("Ingest", flow_type='ingest') >> platform_nodes['AutoLoader']

        # Resize and save
        img_path = f"{output_file.replace('.png', '')}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > 1000 or height > 1000:
                scale = min(1000 / width, 1000 / height)
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                img.save(img_path)
            print(f"   ✓ Saved: {img_path} ({img.width}x{img.height}px)")
            return img_path

    def generate_use_case_diagram(
        self,
        use_case_name: str,
        description: str,
        components: dict,
        output_file: str = "use_case.png"
    ):
        """
        Generate specific use case architecture

        Args:
            use_case_name: Name of use case
            description: Brief description
            components: Dict with layers and components
            output_file: Output filename

        Example:
            components = {
                "input": ["Web Portal", "Mobile App"],
                "agent": ["Intent Understanding", "Reasoning", "Execution"],
                "context": ["Customer Data", "Historical Patterns"],
                "output": ["Recommendations", "Actions"]
            }
        """
        print(f"\n🎯 Generating Use Case: {use_case_name}...")

        with Diagram(
            f"{use_case_name}",
            filename=output_file.replace('.png', ''),
            show=False,
            direction="TB",
            graph_attr=self.icon_gen._get_graph_attr(),
            outformat="png"
        ):
            # Input layer
            inputs = []
            if 'input' in components:
                with Cluster("Input Channels"):
                    for inp in components['input']:
                        icon = self.icon_gen.get_icon('default')
                        inputs.append(Custom(inp, icon))

            # Agent layer
            agent_nodes = []
            if 'agent' in components:
                with Cluster(f"AI Agent - {use_case_name}"):
                    for agent_comp in components['agent']:
                        icon = self.icon_gen.get_icon('mosaic_ai')
                        agent_nodes.append(Custom(agent_comp, icon))

            # Context layer
            contexts = []
            if 'context' in components:
                with Cluster("Context & Data (MCP)"):
                    for ctx in components['context']:
                        icon = self.icon_gen.get_icon(ctx.get('icon', 'delta_lake'))
                        contexts.append(Custom(ctx if isinstance(ctx, str) else ctx['name'], icon))

            # Output layer
            outputs = []
            if 'output' in components:
                with Cluster("Outcomes"):
                    for out in components['output']:
                        icon = self.icon_gen.get_icon('default')
                        outputs.append(Custom(out, icon))

        # Resize and save
        img_path = f"{output_file.replace('.png', '')}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > 1000 or height > 1000:
                scale = min(1000 / width, 1000 / height)
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                img.save(img_path)
            print(f"   ✓ Saved: {img_path} ({img.width}x{img.height}px)")
            return img_path


# Example usage for Energy Australia (demonstrating generic capability)
def generate_energy_australia_example():
    """Generate Energy Australia diagrams using generic generator"""
    gen = AgenticAIGenerator()

    print("=" * 80)
    print("GENERIC AGENTIC AI GENERATOR - ENERGY AUSTRALIA EXAMPLE")
    print("=" * 80)

    # 1. Journey Diagram
    ea_journey = {
        "Phase 1": {
            "title": "Traditional",
            "timeline": "Current State",
            "color": "#666666",
            "fillcolor": "#F5F5F5",
            "components": ["Historical Data", "BI Reports", "Basic ML"]
        },
        "Phase 2": {
            "title": "Predictive AI",
            "timeline": "Q1-Q2 2025",
            "color": "#1B5162",
            "fillcolor": "#F0F8FF",
            "components": ["Delta Lake", "MLflow", "Model Serving"]
        },
        "Phase 3": {
            "title": "Augmented AI",
            "timeline": "Q3-Q4 2025",
            "color": "#618794",
            "fillcolor": "#F0FFFF",
            "components": ["Unity Catalog", "Mosaic AI", "Feature Store"]
        },
        "Phase 4": {
            "title": "Agentic AI",
            "timeline": "2026",
            "color": "#FF3621",
            "fillcolor": "#FFF5F5",
            "components": ["AI Agents", "MCP Protocol", "Autonomous"]
        }
    }

    gen.generate_journey_diagram(
        "Energy Australia",
        ea_journey,
        "ea_journey_generic.png"
    )

    # 2. Full Architecture
    ea_architecture = {
        "data_sources": [
            {"name": "Smart Meters", "icon": "s3_storage"},
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
            {"name": "Customer Service Agent", "icon": "mosaic_ai"},
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
        "ea_architecture_generic.png"
    )

    # 3. Customer Service Agent Use Case
    customer_service_components = {
        "input": ["Web Portal", "Mobile App", "Phone IVR"],
        "agent": ["Intent Understanding", "Reasoning Engine", "Action Execution"],
        "context": [
            {"name": "Customer Profile", "icon": "unity_catalog"},
            {"name": "Usage History", "icon": "delta_lake"},
            {"name": "Billing Data", "icon": "databricks_sql"}
        ],
        "output": ["Recommendations", "Issue Resolution", "Optimization Tips"]
    }

    gen.generate_use_case_diagram(
        "Customer Service Agent",
        "Autonomous customer support with 70% automation",
        customer_service_components,
        "ea_customer_service_generic.png"
    )

    print("\n" + "=" * 80)
    print("✅ GENERATED USING GENERIC SYSTEM")
    print("=" * 80)
    print("\nYou can now generate for ANY company by calling:")
    print("  gen.generate_journey_diagram('Your Company', journey_config, 'output.png')")
    print("  gen.generate_full_architecture('Your Company', arch_config, 'output.png')")
    print("  gen.generate_use_case_diagram('Use Case Name', desc, components, 'output.png')")


if __name__ == "__main__":
    generate_energy_australia_example()
