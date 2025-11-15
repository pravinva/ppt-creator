"""
Energy Australia Agentic AI Journey
Modern architecture diagrams showing the transformation to agentic AI

Key Components:
1. Current State: Traditional ML/Analytics
2. Journey Phases: Predictive -> Augmented -> Autonomous
3. Target State: Full Agentic AI Platform
4. Use Cases: Customer Service, Energy Optimization, Grid Management
"""
from diagram_generator_modern import ModernDatabricksGenerator
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.analytics import Spark
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.custom import Custom
from PIL import Image, ImageDraw, ImageFont
import os


class EnergyAustraliaAgenticAI:
    """Generate Energy Australia Agentic AI Journey diagrams"""

    def __init__(self):
        self.gen = ModernDatabricksGenerator(cloud_provider="azure")

    def generate_agentic_journey_overview(self):
        """Generate overview of agentic AI journey phases"""
        print("\n1. Generating Agentic AI Journey Overview...")

        graph_attr = self.gen._get_modern_graph_attr()
        node_attr = self.gen._get_modern_node_attr()

        with Diagram(
            "Energy Australia - Agentic AI Journey",
            filename="ea_agentic_journey",
            show=False,
            direction="LR",
            graph_attr=graph_attr,
            node_attr=node_attr,
            outformat="png"
        ):
            # Phase 1: Traditional Analytics
            with Cluster(
                "Phase 1: Traditional\n(Current State)",
                graph_attr={"style": "filled", "color": "#666666", "fillcolor": "#F5F5F5"}
            ):
                trad_data = Storage("Historical\nData")
                trad_bi = Rack("BI\nReports")
                trad_ml = Python("Basic ML\nModels")

            # Phase 2: Predictive AI
            with Cluster(
                "Phase 2: Predictive AI\n(Q1-Q2 2025)",
                graph_attr={"style": "filled", "color": "#1B5162", "fillcolor": "#F0F8FF"}
            ):
                pred_delta = DataLakeStorage("Delta Lake\nUnified Data")
                pred_mlflow = Python("MLflow\nModel Registry")
                pred_serving = Rack("Model\nServing")

            # Phase 3: Augmented AI
            with Cluster(
                "Phase 3: Augmented AI\n(Q3-Q4 2025)",
                graph_attr={"style": "filled", "color": "#618794", "fillcolor": "#F0FFFF"}
            ):
                aug_uc = SQL("Unity Catalog\nGovernance")
                aug_genai = Python("Mosaic AI\nGenAI")
                aug_features = Storage("Feature\nStore")

            # Phase 4: Agentic AI
            with Cluster(
                "Phase 4: Agentic AI\n(2026)",
                graph_attr={"style": "filled", "color": "#FF3621", "fillcolor": "#FFF5F5"}
            ):
                agent_platform = Rack("Agentic AI\nPlatform")
                agent_agents = Python("AI Agents\n(Autonomous)")
                agent_mcp = Storage("Model Context\nProtocol")

            # Flow
            trad_data >> Edge(color="#666666", penwidth="2.0") >> pred_delta
            pred_mlflow >> Edge(color="#1B5162", penwidth="2.0") >> aug_genai
            aug_features >> Edge(color="#618794", penwidth="2.0") >> agent_platform
            agent_agents >> Edge(color="#FF3621", penwidth="2.0", style="bold") >> agent_mcp

        img = Image.open("ea_agentic_journey.png")
        img = self.gen._resize_to_max_dimension(img, 1000)
        self.gen.save_diagram(img, "ea_agentic_journey.png")
        print(f"   ✓ Saved: ea_agentic_journey.png ({img.width}x{img.height}px)")
        return img

    def generate_agentic_architecture(self):
        """Generate full agentic AI architecture for Energy Australia"""
        print("\n2. Generating Full Agentic AI Architecture...")

        graph_attr = self.gen._get_modern_graph_attr()
        node_attr = self.gen._get_modern_node_attr()

        with Diagram(
            "Energy Australia - Agentic AI Platform Architecture",
            filename="ea_agentic_architecture",
            show=False,
            direction="LR",
            graph_attr=graph_attr,
            node_attr=node_attr,
            outformat="png"
        ):
            # Data Sources
            with Cluster("Data Sources"):
                smart_meters = Storage("Smart Meters\n(IoT)")
                crm_data = SQL("Customer\nCRM")
                grid_data = Storage("Grid\nOperations")
                weather = Storage("Weather\nData")

            # Ingestion & Storage
            with Cluster("Data Platform\n(Databricks Lakehouse)"):
                autoloader = Spark("AutoLoader\nStreaming")

                with Cluster("Medallion Architecture"):
                    bronze = DataLakeStorage("Bronze\nRaw Data")
                    silver = DataLakeStorage("Silver\nCleansed")
                    gold = DataLakeStorage("Gold\nAggregated")
                    bronze >> silver >> gold

                unity_catalog = SQL("Unity Catalog\nGovernance")

            # AI/ML Layer
            with Cluster("AI/ML Platform"):
                feature_store = Storage("Feature\nStore")
                mlflow = Python("MLflow\nModel Registry")
                mosaic_ai = Python("Mosaic AI\nGenAI Platform")

            # Agentic Layer
            with Cluster("Agentic AI Layer"):
                agent_framework = Rack("Agent\nFramework")

                with Cluster("AI Agents"):
                    customer_agent = Python("Customer\nService Agent")
                    energy_agent = Python("Energy\nOptimization Agent")
                    grid_agent = Python("Grid\nManagement Agent")

                mcp = Storage("Model Context\nProtocol (MCP)")

            # Applications
            with Cluster("Applications"):
                customer_portal = Rack("Customer\nPortal")
                ops_dashboard = Rack("Operations\nDashboard")
                mobile_app = Rack("Mobile\nApp")

            # Connections
            [smart_meters, crm_data, grid_data, weather] >> self.gen._get_modern_edge("Ingest", flow_type='ingest') >> autoloader
            autoloader >> self.gen._get_modern_edge("Store", flow_type='process') >> bronze
            gold >> self.gen._get_modern_edge("Features", flow_type='transform') >> feature_store
            feature_store >> self.gen._get_modern_edge("Train", flow_type='process') >> mlflow
            mlflow >> self.gen._get_modern_edge("GenAI", flow_type='transform') >> mosaic_ai
            mosaic_ai >> self.gen._get_modern_edge("Orchestrate", flow_type='serve') >> agent_framework
            agent_framework >> self.gen._get_modern_edge("Context", flow_type='process') >> mcp
            mcp >> self.gen._get_modern_edge("Execute", flow_type='serve') >> customer_agent
            mcp >> self.gen._get_modern_edge("Execute", flow_type='serve') >> energy_agent
            mcp >> self.gen._get_modern_edge("Execute", flow_type='serve') >> grid_agent
            customer_agent >> self.gen._get_modern_edge("Serve", flow_type='consume') >> customer_portal
            energy_agent >> self.gen._get_modern_edge("Serve", flow_type='consume') >> ops_dashboard
            grid_agent >> self.gen._get_modern_edge("Serve", flow_type='consume') >> mobile_app

        img = Image.open("ea_agentic_architecture.png")
        img = self.gen._resize_to_max_dimension(img, 1000)
        self.gen.save_diagram(img, "ea_agentic_architecture.png")
        print(f"   ✓ Saved: ea_agentic_architecture.png ({img.width}x{img.height}px)")
        return img

    def generate_use_case_architecture(self):
        """Generate specific use case: Customer Service Agent"""
        print("\n3. Generating Customer Service Agent Use Case...")

        graph_attr = self.gen._get_modern_graph_attr()
        node_attr = self.gen._get_modern_node_attr()

        with Diagram(
            "Energy Australia - Customer Service Agent",
            filename="ea_customer_agent",
            show=False,
            direction="TB",
            graph_attr=graph_attr,
            node_attr=node_attr,
            outformat="png"
        ):
            # Customer Interaction
            with Cluster("Customer Channels"):
                web = Rack("Web Portal")
                mobile = Rack("Mobile App")
                phone = Rack("Phone/IVR")

            # Agent Layer
            with Cluster("AI Agent (Autonomous)"):
                agent_brain = Python("Customer Service\nAI Agent")

                with Cluster("Agent Capabilities"):
                    understand = Python("Intent\nUnderstanding")
                    reason = Python("Reasoning\n& Planning")
                    act = Python("Action\nExecution")

            # MCP Integration
            with Cluster("Model Context Protocol"):
                mcp_gateway = Storage("MCP\nGateway")

                with Cluster("Context Sources"):
                    customer_context = SQL("Customer\nProfile")
                    usage_context = Storage("Usage\nHistory")
                    billing_context = SQL("Billing\nData")

            # Databricks Backend
            with Cluster("Databricks Lakehouse"):
                delta_tables = DataLakeStorage("Delta Lake\nCustomer 360")
                genai_models = Python("Mosaic AI\nLLM Models")
                feature_eng = Spark("Feature\nEngineering")

            # Outcomes
            with Cluster("Actions & Outcomes"):
                recommend = Rack("Energy\nRecommendations")
                resolve = Rack("Issue\nResolution")
                optimize = Rack("Usage\nOptimization")

            # Flow
            [web, mobile, phone] >> self.gen._get_modern_edge("Query", flow_type='ingest') >> agent_brain
            agent_brain >> self.gen._get_modern_edge("Process", flow_type='process') >> understand
            understand >> self.gen._get_modern_edge("Analyze", flow_type='process') >> reason
            reason >> self.gen._get_modern_edge("Execute", flow_type='serve') >> act

            act >> self.gen._get_modern_edge("Request Context", flow_type='process') >> mcp_gateway
            mcp_gateway >> self.gen._get_modern_edge("Fetch", flow_type='process') >> customer_context
            mcp_gateway >> self.gen._get_modern_edge("Fetch", flow_type='process') >> usage_context
            mcp_gateway >> self.gen._get_modern_edge("Fetch", flow_type='process') >> billing_context

            [customer_context, usage_context, billing_context] >> self.gen._get_modern_edge("Source", flow_type='transform') >> delta_tables
            delta_tables >> self.gen._get_modern_edge("Features", flow_type='process') >> feature_eng
            feature_eng >> self.gen._get_modern_edge("Inference", flow_type='process') >> genai_models

            genai_models >> self.gen._get_modern_edge("Response", flow_type='serve') >> agent_brain
            agent_brain >> self.gen._get_modern_edge("Deliver", flow_type='consume') >> recommend
            agent_brain >> self.gen._get_modern_edge("Deliver", flow_type='consume') >> resolve
            agent_brain >> self.gen._get_modern_edge("Deliver", flow_type='consume') >> optimize

        img = Image.open("ea_customer_agent.png")
        img = self.gen._resize_to_max_dimension(img, 1000)
        self.gen.save_diagram(img, "ea_customer_agent.png")
        print(f"   ✓ Saved: ea_customer_agent.png ({img.width}x{img.height}px)")
        return img

    def generate_energy_optimization_agent(self):
        """Generate Energy Optimization Agent architecture"""
        print("\n4. Generating Energy Optimization Agent...")

        graph_attr = self.gen._get_modern_graph_attr()
        node_attr = self.gen._get_modern_node_attr()

        with Diagram(
            "Energy Australia - Energy Optimization Agent",
            filename="ea_optimization_agent",
            show=False,
            direction="LR",
            graph_attr=graph_attr,
            node_attr=node_attr,
            outformat="png"
        ):
            # Real-time Data
            with Cluster("Real-time Data Streams"):
                smart_meter = Storage("Smart Meter\nData (IoT)")
                weather_stream = Storage("Weather\nForecasts")
                grid_load = Storage("Grid\nLoad Data")

            # Streaming Processing
            with Cluster("Stream Processing"):
                autoloader = Spark("AutoLoader")
                structured_streaming = Spark("Structured\nStreaming")

            # Delta Lake
            with Cluster("Delta Lake"):
                live_tables = DataLakeStorage("Delta Live\nTables")
                gold_analytics = DataLakeStorage("Gold Layer\nAnalytics")

            # AI Agent
            with Cluster("Optimization Agent"):
                agent_core = Python("Energy\nOptimization Agent")

                with Cluster("Agent Actions"):
                    predict = Python("Demand\nPrediction")
                    optimize = Python("Load\nOptimization")
                    recommend = Python("Customer\nRecommendations")

            # MCP Context
            with Cluster("MCP Context Layer"):
                mcp = Storage("MCP\nProtocol")
                historical = SQL("Historical\nPatterns")
                customer_pref = SQL("Customer\nPreferences")

            # Outcomes
            with Cluster("Automated Actions"):
                pricing = Rack("Dynamic\nPricing")
                alerts = Rack("Customer\nAlerts")
                grid_control = Rack("Grid\nControl")

            # Flow
            [smart_meter, weather_stream, grid_load] >> self.gen._get_modern_edge("Stream", flow_type='ingest') >> autoloader
            autoloader >> self.gen._get_modern_edge("Process", flow_type='process') >> structured_streaming
            structured_streaming >> self.gen._get_modern_edge("Store", flow_type='transform') >> live_tables
            live_tables >> self.gen._get_modern_edge("Aggregate", flow_type='transform') >> gold_analytics

            gold_analytics >> self.gen._get_modern_edge("Analyze", flow_type='process') >> agent_core
            agent_core >> self.gen._get_modern_edge("Context", flow_type='process') >> mcp
            mcp >> self.gen._get_modern_edge("Enrich", flow_type='process') >> historical
            mcp >> self.gen._get_modern_edge("Enrich", flow_type='process') >> customer_pref

            agent_core >> self.gen._get_modern_edge("Execute", flow_type='serve') >> predict
            agent_core >> self.gen._get_modern_edge("Execute", flow_type='serve') >> optimize
            agent_core >> self.gen._get_modern_edge("Execute", flow_type='serve') >> recommend

            predict >> self.gen._get_modern_edge("Apply", flow_type='consume') >> pricing
            optimize >> self.gen._get_modern_edge("Send", flow_type='consume') >> alerts
            recommend >> self.gen._get_modern_edge("Control", flow_type='consume') >> grid_control

        img = Image.open("ea_optimization_agent.png")
        img = self.gen._resize_to_max_dimension(img, 1000)
        self.gen.save_diagram(img, "ea_optimization_agent.png")
        print(f"   ✓ Saved: ea_optimization_agent.png ({img.width}x{img.height}px)")
        return img

    def generate_all(self):
        """Generate all Energy Australia Agentic AI diagrams"""
        print("=" * 80)
        print("ENERGY AUSTRALIA - AGENTIC AI JOURNEY")
        print("=" * 80)
        print("\nGenerating modern architecture diagrams with 2025 Databricks style...")

        diagrams = []

        # Generate all diagrams
        diagrams.append(self.generate_agentic_journey_overview())
        diagrams.append(self.generate_agentic_architecture())
        diagrams.append(self.generate_use_case_architecture())
        diagrams.append(self.generate_energy_optimization_agent())

        print("\n" + "=" * 80)
        print("✅ ALL ENERGY AUSTRALIA DIAGRAMS GENERATED!")
        print("=" * 80)
        print("\nGenerated files:")
        print("  1. ea_agentic_journey.png - Journey overview (4 phases)")
        print("  2. ea_agentic_architecture.png - Full platform architecture")
        print("  3. ea_customer_agent.png - Customer service agent use case")
        print("  4. ea_optimization_agent.png - Energy optimization agent")
        print("\nKey Features:")
        print("  • Modern Databricks 2025 style (Navy + Orange)")
        print("  • Azure-focused architecture (ADLS Gen2)")
        print("  • Agentic AI with Model Context Protocol (MCP)")
        print("  • Real-world Energy Australia use cases")
        print("  • Production-ready architecture patterns")

        return diagrams


if __name__ == "__main__":
    ea = EnergyAustraliaAgenticAI()
    ea.generate_all()
