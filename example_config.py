"""
Example Configuration for Databricks Presentation Creator

This file shows example configurations for different Databricks workspace setups.
Copy and modify as needed for your environment.
"""

# Example 1: Standard Databricks Foundation Models Endpoint
CLAUDE_ENDPOINT_STANDARD = {
    'pattern': '/serving-endpoints/databricks-claude-sonnet-4-5/invocations',
    'description': 'Standard Databricks Foundation Models endpoint for Claude'
}

# Example 2: Custom Endpoint Name
CLAUDE_ENDPOINT_CUSTOM = {
    'pattern': '/serving-endpoints/my-custom-claude-endpoint/invocations',
    'description': 'Custom endpoint name configured in your workspace'
}

# Example 3: API 2.0 Format
CLAUDE_ENDPOINT_API_V2 = {
    'pattern': '/api/2.0/serving-endpoints/claude-sonnet-4-5/invocations',
    'description': 'Using API 2.0 path format'
}

# Databricks Brand Colors (for reference)
BRAND_COLORS = {
    'primary_red': '#FF3621',
    'dark_navy': '#1B3139',
    'medium_navy': '#2C4A56',
    'light_blue': '#00A4E4',
    'success_green': '#00C853',
    'warning_orange': '#FF9800',
    'error_red': '#F44336',
    'background_gray': '#F5F5F5',
    'text_dark': '#1B3139',
    'text_medium': '#666666',
    'text_light': '#999999',
}

# Diagram Colors
DIAGRAM_COLORS = {
    'bronze': '#CD7F32',
    'silver': '#C0C0C0',
    'gold': '#FFD700',
    'white': '#FFFFFF',
    'light_gray': '#E8E8E8',
    'dark_gray': '#666666',
}

# Default Presentation Settings
DEFAULT_SETTINGS = {
    'num_slides': 5,
    'min_slides': 1,
    'max_slides': 20,
    'default_sections': ['Introduction', 'Architecture', 'Implementation', 'Next Steps'],
    'diagram_width': 1280,
    'diagram_height': 720,
}

# Claude API Settings
CLAUDE_SETTINGS = {
    'model': 'claude-sonnet-4-5',
    'max_tokens': 4096,
    'temperature': 0.7,
    'timeout_seconds': 120,
}

# Example Prompts for Different Use Cases
EXAMPLE_PROMPTS = {
    'data_platform': """
        Create a presentation about building a modern data platform on Databricks
        for a large enterprise. Include data governance with Unity Catalog,
        medallion architecture for data quality, and integration patterns.
    """,

    'ml_platform': """
        Design an MLOps platform presentation for a financial services company.
        Cover the full ML lifecycle: feature engineering, model training with
        Databricks ML Runtime, deployment, and monitoring with MLflow.
    """,

    'migration': """
        Present a migration strategy from legacy data warehouse to Databricks
        Lakehouse Platform. Include TCO comparison, migration approach,
        risk mitigation, and timeline. Focus on Delta Lake benefits.
    """,

    'real_time': """
        Create a real-time analytics solution architecture using Databricks
        for an e-commerce platform. Include streaming with Auto Loader,
        Delta Live Tables, and real-time dashboards.
    """,

    'retail': """
        Solutions architecture for a retail customer analytics platform.
        Include customer 360 view, personalization engine, inventory
        optimization, and demand forecasting with Databricks ML.
    """,

    'healthcare': """
        HIPAA-compliant healthcare analytics platform on Databricks.
        Cover data security, Unity Catalog for governance, patient
        analytics, and clinical decision support systems.
    """,
}

# Workspace Configuration Examples
WORKSPACE_CONFIGS = {
    'aws': {
        'host_pattern': 'https://your-workspace.cloud.databricks.com',
        'region': 'us-west-2',
        'cloud_provider': 'AWS'
    },
    'azure': {
        'host_pattern': 'https://adb-1234567890123456.7.azuredatabricks.net',
        'region': 'eastus',
        'cloud_provider': 'Azure'
    },
    'gcp': {
        'host_pattern': 'https://1234567890123456.7.gcp.databricks.com',
        'region': 'us-central1',
        'cloud_provider': 'GCP'
    }
}
