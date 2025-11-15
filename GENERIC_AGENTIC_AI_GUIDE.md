# Generic Agentic AI Architecture Generator

A flexible, prompt-based system to generate **Agentic AI architecture diagrams and presentations** for **ANY company or use case**.

## Overview

This system allows you to create professional Databricks Agentic AI architectures for any company by simply providing:
- Company name
- Use case descriptions
- Architecture components
- Journey phases

**Always uses authentic Databricks 112x112 icons** from `databricks_assets/`.

## Key Features

✅ **Generic & Reusable** - Works for any company/industry
✅ **Modern Databricks Style** - 2025 style guide (Navy + Orange)
✅ **Authentic Icons** - Uses real Databricks 112x112 PNG icons
✅ **Automated PPTX** - Generates PowerPoint presentations
✅ **Prompt-Based** - Easy configuration with Python dicts
✅ **Production-Ready** - Max 1000px, white backgrounds, 1px connectors

## Quick Start

### 1. Generate Architecture Diagrams

```python
from agentic_ai_generator import AgenticAIGenerator

gen = AgenticAIGenerator()

# Define your journey phases
journey_config = {
    "Phase 1": {
        "title": "Current State",
        "timeline": "Today",
        "color": "#666666",
        "fillcolor": "#F5F5F5",
        "components": ["Legacy Systems", "Manual Processes"]
    },
    "Phase 2": {
        "title": "Predictive AI",
        "timeline": "Q1-Q2 2025",
        "color": "#1B5162",
        "fillcolor": "#F0F8FF",
        "components": ["Delta Lake", "MLflow", "Model Serving"]
    },
    # Add more phases...
}

# Generate journey diagram
gen.generate_journey_diagram(
    "Your Company Name",
    journey_config,
    "your_journey.png"
)
```

### 2. Generate Full Architecture

```python
architecture_config = {
    "data_sources": [
        {"name": "IoT Sensors", "icon": "kafka"},
        {"name": "Customer DB", "icon": "azure_blob"}
    ],
    "platform_components": [
        {"name": "AutoLoader", "icon": "autoloader"},
        {"name": "Delta Lake", "icon": "delta_lake"},
        {"name": "Unity Catalog", "icon": "unity_catalog"}
    ],
    "ai_agents": [
        {"name": "Customer Agent", "icon": "mosaic_ai"},
        {"name": "Operations Agent", "icon": "mosaic_ai"}
    ],
    "applications": [
        {"name": "Web Portal", "icon": "tableau"},
        {"name": "Mobile App", "icon": "powerbi"}
    ]
}

gen.generate_full_architecture(
    "Your Company Name",
    architecture_config,
    "your_architecture.png"
)
```

### 3. Generate Use Case Diagrams

```python
use_case_components = {
    "input": ["Web", "Mobile", "API"],
    "agent": ["Intent Understanding", "Reasoning", "Execution"],
    "context": [
        {"name": "User Profile", "icon": "unity_catalog"},
        {"name": "Historical Data", "icon": "delta_lake"}
    ],
    "output": ["Recommendations", "Actions", "Insights"]
}

gen.generate_use_case_diagram(
    "Your Use Case Name",
    "Description of use case",
    use_case_components,
    "your_use_case.png"
)
```

### 4. Generate PowerPoint Presentation

```python
from agentic_ai_pptx_generator import AgenticAIPPTXGenerator

pptx_gen = AgenticAIPPTXGenerator()

pptx_config = {
    "subtitle": "Your Custom Subtitle",
    "slides": [
        {
            "type": "diagram",
            "title": "Journey Overview",
            "image": "your_journey.png",
            "subtitle": "Transformation roadmap"
        },
        {
            "type": "content",
            "title": "Benefits",
            "content": [
                "• 50% cost reduction",
                "• 70% automation",
                "• $10M annual savings"
            ]
        },
        {
            "type": "diagram",
            "title": "Architecture",
            "image": "your_architecture.png"
        }
    ]
}

pptx_gen.generate_presentation(
    "Your Company Name",
    pptx_config,
    "Your_Presentation.pptx"
)
```

## Available Databricks Icons

The system auto-discovers **28+ authentic Databricks icons**:

### Product Icons (112x112 PNG)
- `databricks_sql` - Databricks SQL
- `delta_lake` - Delta Lake
- `autoloader` - AutoLoader
- `mlflow` - MLflow
- `unity_catalog` - Unity Catalog
- `mosaic_ai` - Mosaic AI
- `feature_store` - Feature Store
- `workflows` - Workflows
- `sql_warehouse` - SQL Warehouse
- `lakehouse` - Lakehouse

### Cloud Service Icons
- `s3_storage` - AWS S3
- `azure_blob` - Azure Blob Storage
- `gcp_storage` - GCP Storage
- `kafka` - Apache Kafka
- `snowflake` - Snowflake

### BI Tool Icons
- `tableau` - Tableau
- `powerbi` - Power BI
- `looker` - Looker

### Default
- `default` - Databricks logo (fallback)

**Note**: All icons are extracted from official Databricks templates (112x112 PNG format).

## Example Use Cases

### Retail Company

```python
gen = AgenticAIGenerator()

retail_journey = {
    "Phase 1": {
        "title": "Traditional",
        "timeline": "Current",
        "color": "#666666",
        "fillcolor": "#F5F5F5",
        "components": ["POS Systems", "Excel Reports", "Manual Inventory"]
    },
    "Phase 2": {
        "title": "Predictive",
        "timeline": "2025 H1",
        "color": "#1B5162",
        "fillcolor": "#F0F8FF",
        "components": ["Delta Lake", "Demand Forecasting", "Dynamic Pricing"]
    },
    "Phase 3": {
        "title": "Augmented",
        "timeline": "2025 H2",
        "color": "#618794",
        "fillcolor": "#F0FFFF",
        "components": ["Unity Catalog", "GenAI Chatbot", "Personalization"]
    },
    "Phase 4": {
        "title": "Agentic",
        "timeline": "2026",
        "color": "#FF3621",
        "fillcolor": "#FFF5F5",
        "components": ["Inventory Agent", "Pricing Agent", "Customer Agent"]
    }
}

gen.generate_journey_diagram("Retail Corp", retail_journey, "retail_journey.png")
```

### Financial Services

```python
finance_architecture = {
    "data_sources": [
        {"name": "Trading Systems", "icon": "kafka"},
        {"name": "Customer CRM", "icon": "snowflake"},
        {"name": "Market Data", "icon": "s3_storage"}
    ],
    "platform_components": [
        {"name": "AutoLoader", "icon": "autoloader"},
        {"name": "Delta Lake", "icon": "delta_lake"},
        {"name": "MLflow", "icon": "mlflow"}
    ],
    "ai_agents": [
        {"name": "Fraud Detection Agent", "icon": "mosaic_ai"},
        {"name": "Trading Agent", "icon": "mosaic_ai"},
        {"name": "Customer Service Agent", "icon": "mosaic_ai"}
    ],
    "applications": [
        {"name": "Trading Platform", "icon": "tableau"},
        {"name": "Mobile Banking", "icon": "powerbi"}
    ]
}

gen.generate_full_architecture(
    "Financial Services Co",
    finance_architecture,
    "finance_architecture.png"
)
```

### Healthcare

```python
healthcare_use_case = {
    "input": ["Patient Portal", "Provider App", "EHR System"],
    "agent": [
        "Symptom Analysis",
        "Treatment Planning",
        "Appointment Scheduling"
    ],
    "context": [
        {"name": "Patient Records", "icon": "unity_catalog"},
        {"name": "Medical History", "icon": "delta_lake"},
        {"name": "Clinical Guidelines", "icon": "databricks_sql"}
    ],
    "output": [
        "Diagnosis Support",
        "Treatment Plans",
        "Follow-up Recommendations"
    ]
}

gen.generate_use_case_diagram(
    "Clinical Decision Support Agent",
    "AI-powered clinical decision support",
    healthcare_use_case,
    "healthcare_agent.png"
)
```

## Customization Options

### Colors

You can customize phase colors in journey diagrams:

```python
"Phase 1": {
    "color": "#1B3139",      # Border color
    "fillcolor": "#F5F5F5",  # Background fill
    # ...
}
```

**Recommended Databricks Colors:**
- Dark Navy: `#1B3139`
- Medium Blue: `#1B5162`
- Light Blue: `#618794`
- Orange: `#FF3621`
- Green: `#00A972`
- Gray: `#666666`

### Slide Types

Two types of slides in PPTX presentations:

1. **Diagram Slide**
```python
{
    "type": "diagram",
    "title": "Slide Title",
    "image": "path/to/diagram.png",
    "subtitle": "Optional subtitle"
}
```

2. **Content Slide**
```python
{
    "type": "content",
    "title": "Slide Title",
    "content": [
        "• Main point",
        "  - Sub-point (indented)",
        "",  # Blank line for spacing
        "• Another point"
    ]
}
```

## Files

### Core Files

1. **`agentic_ai_generator.py`** - Generic diagram generator
   - `generate_journey_diagram()` - 4-phase journey
   - `generate_full_architecture()` - Complete platform
   - `generate_use_case_diagram()` - Specific use cases

2. **`agentic_ai_pptx_generator.py`** - Generic PPTX generator
   - `generate_presentation()` - Complete presentation
   - `add_diagram_slide()` - Add diagram slide
   - `add_content_slide()` - Add text slide

3. **`diagram_generator_with_custom_icons.py`** - Icon management
   - Auto-discovers Databricks icons
   - Maps icon names to files
   - Uses 112x112 PNG format

### Example Files (Energy Australia)

These are **examples** showing how to use the generic system:

- `energy_australia_agentic_ai.py` - EA-specific implementation
- `energy_australia_pptx_generator.py` - EA-specific PPTX
- `ea_*.png` - Generated EA diagrams
- `Energy_Australia_*.pptx` - Generated EA presentations

**You can create similar files for YOUR company!**

## Best Practices

### 1. Icon Selection

Always use Databricks icons when available:
- For Databricks products: Use product-specific icons
- For cloud services: Use cloud service icons
- For BI tools: Use BI tool icons
- For generic components: Use `default` Databricks logo

### 2. Diagram Sizing

All diagrams auto-resize to max 1000px (following Databricks guidelines):
- Maintains aspect ratio
- White background (never transparent)
- High quality (300 DPI)

### 3. Journey Phases

Typical 4-phase journey:
1. **Current State** - Traditional/legacy systems
2. **Predictive AI** - ML models, forecasting
3. **Augmented AI** - GenAI, human-in-loop
4. **Agentic AI** - Autonomous agents

### 4. Architecture Layers

Recommended architecture layers:
- **Data Sources** - Where data comes from
- **Platform Components** - Databricks lakehouse
- **AI Agents** - Autonomous agents
- **Applications** - User-facing apps

### 5. Use Case Components

Standard use case structure:
- **Input** - How users interact
- **Agent** - AI agent capabilities
- **Context** - Data sources via MCP
- **Output** - Results and actions

## Advanced Usage

### Custom Icon Mapping

Add your own icon mappings:

```python
from diagram_generator_with_custom_icons import ModernDatabricksIconGenerator

icon_gen = ModernDatabricksIconGenerator()

# Add custom mapping
icon_gen.icon_mapping['my_service'] = 'path/to/custom_icon.png'

# Use in diagram
gen = AgenticAIGenerator()
gen.icon_gen = icon_gen
```

### Multi-Page Presentations

Create complex presentations:

```python
pptx_config = {
    "subtitle": "Complete Transformation",
    "slides": [
        {"type": "diagram", "title": "Journey", "image": "journey.png"},
        {"type": "content", "title": "Phase 1", "content": [...]},
        {"type": "diagram", "title": "Architecture", "image": "arch.png"},
        {"type": "content", "title": "Use Cases", "content": [...]},
        {"type": "diagram", "title": "Use Case 1", "image": "uc1.png"},
        {"type": "diagram", "title": "Use Case 2", "image": "uc2.png"},
        {"type": "content", "title": "ROI", "content": [...]},
        {"type": "content", "title": "Next Steps", "content": [...]}
    ]
}
```

### Batch Generation

Generate for multiple companies:

```python
companies = ["Retail Corp", "Finance Inc", "Healthcare LLC"]

for company in companies:
    gen = AgenticAIGenerator()

    # Customize config per company
    journey_config = get_journey_config(company)

    gen.generate_journey_diagram(
        company,
        journey_config,
        f"{company.lower().replace(' ', '_')}_journey.png"
    )
```

## Style Guide Compliance

All generated diagrams follow **Databricks 2025 Style Guide**:

✅ Max 1000px width or height
✅ DM Sans typography (simulated)
✅ Navy (#1B3139) + Orange (#FF3621) color scheme
✅ 1px connector lines
✅ White background (never transparent)
✅ 112x112 PNG icons
✅ Proper spacing and alignment
✅ High quality (300 DPI)

## Troubleshooting

### Issue: Icon not found

**Solution**: Check available icons:
```python
gen = AgenticAIGenerator()
print(gen.icon_gen.icon_mapping.keys())
```

Use `default` icon as fallback.

### Issue: Diagram too large

**Solution**: Diagrams auto-resize to 1000px max. If still too large, reduce number of components.

### Issue: PPTX image not appearing

**Solution**: Ensure image file exists before generating PPTX:
```python
import os
if os.path.exists("your_diagram.png"):
    # Generate PPTX
```

## Support

For issues or questions:
1. Check this guide
2. Review example files (Energy Australia)
3. Inspect generated diagrams
4. Verify icon availability

## License

Uses official Databricks icons and templates.
For internal use only.

---

**Version**: 1.0
**Last Updated**: 2025-11-15
**Status**: Production Ready ✅
