"""
Complete End-to-End Professional Agentic AI Presentation Generator
Demonstrates the full workflow from diagrams to PowerPoint

Works for ANY company - Energy Australia used as example
"""
from professional_agentic_ai_generator import ProfessionalAgenticAIGenerator
from agentic_ai_pptx_generator import AgenticAIPPTXGenerator


def generate_energy_australia_complete():
    """
    Generate complete professional presentation for Energy Australia
    This demonstrates the FULL workflow for ANY company
    """
    print("=" * 80)
    print("COMPLETE PROFESSIONAL AGENTIC AI PRESENTATION GENERATOR")
    print("=" * 80)
    print("\nCompany: Energy Australia (example - works for ANY company)")
    print("Output: Professional diagrams + PowerPoint presentation\n")

    # Initialize generators
    diagram_gen = ProfessionalAgenticAIGenerator()
    pptx_gen = AgenticAIPPTXGenerator()

    company_name = "Energy Australia"

    # ==========================================================================
    # STEP 1: Generate Journey Diagram
    # ==========================================================================
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING JOURNEY DIAGRAM")
    print("=" * 80)

    journey_config = {
        "Phase 1": {
            "title": "Traditional Analytics",
            "timeline": "Current State",
            "components": [
                {"name": "Historical Data", "icon": "delta_lake"},
                {"name": "BI Dashboards", "icon": "tableau"},
                {"name": "Basic ML", "icon": "mlflow"}
            ]
        },
        "Phase 2": {
            "title": "Predictive AI",
            "timeline": "Q1-Q2 2025",
            "components": [
                {"name": "Delta Lake", "icon": "delta_lake"},
                {"name": "MLflow", "icon": "mlflow"},
                {"name": "Demand Forecasting", "icon": "workflows"}
            ]
        },
        "Phase 3": {
            "title": "Augmented AI",
            "timeline": "Q3-Q4 2025",
            "components": [
                {"name": "Unity Catalog", "icon": "unity_catalog"},
                {"name": "Mosaic AI", "icon": "mosaic_ai"},
                {"name": "GenAI Chatbot", "icon": "mosaic_ai"}
            ]
        },
        "Phase 4": {
            "title": "Agentic AI",
            "timeline": "2026",
            "components": [
                {"name": "Customer Agent", "icon": "mosaic_ai"},
                {"name": "Energy Agent", "icon": "mosaic_ai"},
                {"name": "Grid Agent", "icon": "mosaic_ai"}
            ]
        }
    }

    journey_file = diagram_gen.generate_journey_diagram(
        company_name,
        journey_config,
        "ea_journey_final.png"
    )

    # ==========================================================================
    # STEP 2: Generate Architecture Diagram
    # ==========================================================================
    print("\n" + "=" * 80)
    print("STEP 2: GENERATING ARCHITECTURE DIAGRAM")
    print("=" * 80)

    architecture_config = {
        "data_sources": [
            {"name": "Smart Meters", "icon": "kafka"},
            {"name": "CRM System", "icon": "azure_blob"},
            {"name": "Grid Data", "icon": "s3"}
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

    architecture_file = diagram_gen.generate_full_architecture(
        company_name,
        architecture_config,
        "ea_architecture_final.png"
    )

    # ==========================================================================
    # STEP 3: Generate PowerPoint Presentation
    # ==========================================================================
    print("\n" + "=" * 80)
    print("STEP 3: GENERATING POWERPOINT PRESENTATION")
    print("=" * 80)

    pptx_config = {
        "subtitle": "Agentic AI Journey\\nTransformation Roadmap 2025-2026",
        "slides": [
            # Slide 1: Journey Overview
            {
                "type": "diagram",
                "title": "Agentic AI Journey - 4 Phase Transformation",
                "image": journey_file,
                "subtitle": "Traditional → Predictive → Augmented → Agentic"
            },

            # Slide 2: Journey Phases Explained
            {
                "type": "content",
                "title": "Journey Phases",
                "content": [
                    "• Phase 1: Traditional Analytics (Current)",
                    "  - Historical data analysis",
                    "  - Static BI dashboards",
                    "  - Basic machine learning models",
                    "",
                    "• Phase 2: Predictive AI (Q1-Q2 2025)",
                    "  - Delta Lake foundation",
                    "  - MLflow for model management",
                    "  - Demand forecasting & optimization",
                    "",
                    "• Phase 3: Augmented AI (Q3-Q4 2025)",
                    "  - Unity Catalog for governance",
                    "  - Mosaic AI for GenAI capabilities",
                    "  - Human-in-the-loop workflows",
                    "",
                    "• Phase 4: Agentic AI (2026)",
                    "  - Autonomous AI agents",
                    "  - MCP protocol integration",
                    "  - Self-improving systems"
                ]
            },

            # Slide 3: Full Architecture
            {
                "type": "diagram",
                "title": "Complete Agentic AI Platform Architecture",
                "image": architecture_file,
                "subtitle": "End-to-end platform with autonomous AI agents"
            },

            # Slide 4: Use Cases
            {
                "type": "content",
                "title": "Key Use Cases",
                "content": [
                    "• Customer Service Agent",
                    "  - 70% automation rate",
                    "  - 50% faster response times",
                    "  - 24/7 autonomous support",
                    "",
                    "• Energy Optimization Agent",
                    "  - Real-time demand prediction",
                    "  - Dynamic pricing optimization",
                    "  - Grid load balancing",
                    "",
                    "• Grid Management Agent",
                    "  - Predictive maintenance",
                    "  - Fault detection & prevention",
                    "  - Autonomous remediation"
                ]
            },

            # Slide 5: Technology Stack
            {
                "type": "content",
                "title": "Databricks Platform Components",
                "content": [
                    "• Data Foundation",
                    "  - AutoLoader: Incremental data ingestion",
                    "  - Delta Lake: ACID transactions & time travel",
                    "  - Unity Catalog: Unified governance",
                    "",
                    "• AI & ML Capabilities",
                    "  - MLflow: Experiment tracking & model registry",
                    "  - Feature Store: Centralized feature management",
                    "  - Mosaic AI: GenAI & LLM capabilities",
                    "",
                    "• Agent Framework",
                    "  - Model Context Protocol (MCP)",
                    "  - Autonomous reasoning & execution",
                    "  - Real-time decision making"
                ]
            },

            # Slide 6: Business Impact & ROI
            {
                "type": "content",
                "title": "Business Impact & ROI",
                "content": [
                    "• Investment: $6.75M over 3 years",
                    "",
                    "• Annual Benefits (Year 3): $19M",
                    "  - Customer service cost reduction: $6M",
                    "  - Energy optimization savings: $5M",
                    "  - Churn reduction revenue: $3M",
                    "  - Grid infrastructure savings: $3M",
                    "  - Operational efficiency: $2M",
                    "",
                    "• ROI Metrics",
                    "  - Payback period: 15 months",
                    "  - 3-year ROI: 180%",
                    "  - 5-year NPV: $42M",
                    "  - IRR: 65%"
                ]
            },

            # Slide 7: Implementation Timeline
            {
                "type": "content",
                "title": "Implementation Timeline",
                "content": [
                    "• Q1 2025: Foundation",
                    "  - Databricks platform setup",
                    "  - Delta Lake & Unity Catalog deployment",
                    "  - Initial data migration",
                    "",
                    "• Q2 2025: Predictive AI",
                    "  - MLflow implementation",
                    "  - Demand forecasting models",
                    "  - First production ML models",
                    "",
                    "• Q3-Q4 2025: Augmented AI",
                    "  - Mosaic AI integration",
                    "  - GenAI chatbot pilot",
                    "  - Human-in-loop workflows",
                    "",
                    "• 2026: Agentic AI",
                    "  - Autonomous agent deployment",
                    "  - MCP protocol integration",
                    "  - Full production rollout"
                ]
            },

            # Slide 8: Next Steps
            {
                "type": "content",
                "title": "Next Steps",
                "content": [
                    "• Immediate Actions (Next 30 Days)",
                    "  - Approve business case & budget",
                    "  - Kickoff Databricks POC",
                    "  - Assemble core project team",
                    "",
                    "• Short-Term (Q1 2025)",
                    "  - Platform architecture design",
                    "  - Data migration strategy",
                    "  - Initial use case prioritization",
                    "",
                    "• Medium-Term (2025)",
                    "  - Phase 2 & 3 implementation",
                    "  - Team training & enablement",
                    "  - Governance framework",
                    "",
                    "• Long-Term (2026+)",
                    "  - Agentic AI deployment",
                    "  - Scale to additional use cases",
                    "  - Continuous optimization"
                ]
            }
        ]
    }

    pptx_file = pptx_gen.generate_presentation(
        company_name,
        pptx_config,
        f"{company_name.replace(' ', '_')}_Agentic_AI_Complete.pptx"
    )

    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    print("\n" + "=" * 80)
    print("✅ COMPLETE PRESENTATION GENERATED!")
    print("=" * 80)
    print(f"\nGenerated Files:")
    print(f"  📊 Journey Diagram: {journey_file}")
    print(f"  🏗️  Architecture Diagram: {architecture_file}")
    print(f"  📄 PowerPoint: {pptx_file}")
    print("\nKey Features:")
    print("  ✓ Professional swim-lane diagrams")
    print("  ✓ Real arrows showing data flow")
    print("  ✓ Authentic Databricks 112x112 icons")
    print("  ✓ 8 comprehensive slides")
    print("  ✓ Complete business case (journey, architecture, ROI, timeline)")
    print("\nThis workflow works for ANY company!")
    print("Just modify the configs for your specific use case.")


def generate_retail_example():
    """
    Quick example for a DIFFERENT company (Retail)
    Shows how generic the system is
    """
    print("\n\n" + "=" * 80)
    print("BONUS: RETAIL COMPANY EXAMPLE")
    print("=" * 80)
    print("\nGenerating for a completely different industry...\n")

    gen = ProfessionalAgenticAIGenerator()

    retail_journey = {
        "Phase 1": {
            "title": "Traditional",
            "timeline": "Current",
            "components": [
                {"name": "POS Systems", "icon": "default"},
                {"name": "Excel Reports", "icon": "tableau"}
            ]
        },
        "Phase 2": {
            "title": "Predictive",
            "timeline": "2025 H1",
            "components": [
                {"name": "Delta Lake", "icon": "delta_lake"},
                {"name": "Demand Forecast", "icon": "mlflow"}
            ]
        },
        "Phase 3": {
            "title": "Augmented",
            "timeline": "2025 H2",
            "components": [
                {"name": "Unity Catalog", "icon": "unity_catalog"},
                {"name": "GenAI Chatbot", "icon": "mosaic_ai"}
            ]
        },
        "Phase 4": {
            "title": "Agentic",
            "timeline": "2026",
            "components": [
                {"name": "Inventory Agent", "icon": "mosaic_ai"},
                {"name": "Pricing Agent", "icon": "mosaic_ai"}
            ]
        }
    }

    gen.generate_journey_diagram(
        "Retail Corporation",
        retail_journey,
        "retail_journey_example.png"
    )

    print("\n✅ Retail example generated!")
    print("The same code works for Energy, Retail, Finance, Healthcare, etc.")


if __name__ == "__main__":
    # Generate complete Energy Australia presentation
    generate_energy_australia_complete()

    # Show it works for other companies too
    generate_retail_example()

    print("\n" + "=" * 80)
    print("🎉 ALL DONE!")
    print("=" * 80)
    print("\nYou now have:")
    print("  1. Professional diagram generator (swim lanes + real arrows)")
    print("  2. Generic system (works for ANY company)")
    print("  3. PowerPoint integration (automated presentations)")
    print("  4. Complete examples (Energy Australia + Retail)")
    print("\nReady for production use! ✅")
